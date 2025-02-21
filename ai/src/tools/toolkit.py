import io
import os
import base64
import hashlib
import diskcache as db
from typing import Type
from pydantic import BaseModel
from crewai.tools import BaseTool
from PIL import Image
from ai.src.utils.azure_llm import AzureLLMConfig
from src.core.paths import TEST_PLAN
from src.core.paths import FUNCTION
from ai.src.tools.functions import FunctionMapping
from ai.src.tools.interface import FunctionMapInterface, ReadTestPlanToolInterface, ImageVisionToolInterface


class ImageVisionTool(BaseTool):

    name: str = 'Image Vision Tool'
    description: str = 'Image Vision Tool'
    image_path: Type[BaseModel] = ImageVisionToolInterface
    azure_client = AzureLLMConfig()

    def __compress_image_to_base64(self, image_path: str, image_format: str = 'JPEG' or 'PNG') -> str:

        with Image.open(image_path) as img:
            buffer = io.BytesIO()
            img.save(buffer, image_format=image_format, quality=100)
            return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def _run(self, **kwargs: any) -> None:
        llm = self.azure_client.azure_llm
        image_base64 = self.__compress_image_to_base64(kwargs.get('image_path'))
        response = llm.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                        },
                    ],
                }
            ],
            max_tokens=15000,
            temperature=self.azure_client.temperature
        )
        return response.choices[0].message.content


class FunctionMappingTool(BaseTool):

    name: str = "Function Mapping Tool"
    description: str = "getting the relevant functions"
    query: Type[BaseModel] = FunctionMapInterface

    def _run(self, query: str) -> str:

        function_mapping = FunctionMapping()
        function = function_mapping.get_all_mappings()

        if function:
            return function

        return "No matching function found."


class ReadTestPlanTool(BaseTool):

    name: str = "Function Mapping Tool"
    description: str = "getting the relevant functions"
    test_plan: Type[BaseModel] = ReadTestPlanToolInterface

    @staticmethod
    def read_test_plan(path: str):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def _run(self, test_plan: str) -> str:
        if isinstance(test_plan, dict):
            test_plan.get("query", test_plan)
        return self.read_test_plan(TEST_PLAN)


class FunctionMappingForFileReadTool:

    def __init__(self, base_dir: str) -> None:
        self.base_dir = base_dir
        self.cache = db.Cache(f"{FUNCTION}/func_cache_db")

    def get_file_hash(self):
        """Compute SHA256 hash of a directory path to use as a cache key."""
        return hashlib.sha256(self.base_dir.encode()).hexdigest()

    def get_all_python_files(self):
        """Retrieve Python files from cache if available, otherwise scan and cache them."""
        dir_hash = self.get_file_hash()

        if dir_hash in self.cache:
            print("Using cached file list...")
            return self.cache[dir_hash]

        print("Scanning directory for Python files...")
        py_files = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

        # Store in cache
        self.cache[dir_hash] = py_files
        return py_files
