import os
import ast
import hashlib
import diskcache as db
from typing import Any, Dict, Tuple

from crewai.crews import CrewOutput

from ai.src.crews.mapping_crew.crew import MappingCrew
from src.core.paths import FUNCTIONS_INDEX
from src.utils.azure_config import AzureOpenAIConfig


class FunctionMapping(AzureOpenAIConfig):

    def __init__(self, base_dir=FUNCTIONS_INDEX) -> None:
        self.cache = db.Cache(f"{base_dir}/func_cache_db")
        self.base_dir = base_dir
        self.client = MappingCrew()  # ✅ Using CrewAI agent for function mapping

    @property
    def index_functions(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        return self.scan_directory()

    def scan_directory(self) -> dict:
        """Scans Python files in base directory, extracts function names and docstrings, and caches them."""
        files_functions = {}
        for root, _, files in os.walk(self.base_dir):
            if '.venv' in root or 'venv' in root:
                continue
            for file in files:
                if file.endswith(".py"):
                    file_path: Any = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(file_path, self.base_dir))[0].replace(os.sep, ".")
                    extracted_functions = self.__extract_functions_with_cache(file_path, module_name)
                    files_functions[module_name] = extracted_functions
        return files_functions

    def __extract_functions_with_cache(self, file_path: str, module_name: str) -> Dict:
        """Extracts function names and docstrings with caching."""
        last_modified = os.path.getmtime(file_path)
        cache_key = self.__generate_cache_key(file_path)

        if cache_key in self.cache and self.cache[cache_key]['timestamp'] == last_modified:
            return self.cache[cache_key]['functions']

        functions = self.__extract_functions(file_path, module_name)
        self.cache[cache_key] = {'functions': functions, 'timestamp': last_modified}
        return functions

    @staticmethod
    def __extract_functions(file_path: str, module_name: str) -> Dict[str, Tuple[str, str]]:
        """Extracts function names and their docstrings from a Python file."""
        functions = {}
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""
                functions[node.name] = (module_name, docstring)
        return functions

    @staticmethod
    def __generate_cache_key(file_path: str) -> str:
        """Generates a unique cache key based on the file path."""
        return hashlib.md5(file_path.encode()).hexdigest()

    def find_best_function(self, user_input: str) -> CrewOutput:

        function_index = {fn: doc for module in self.index_functions.values() for fn, (_, doc) in module.items()}

        response = self.client.execute(
            user_input=user_input,
            function_index=function_index
        )
        return response

    def execute_function(self, user_input: str) -> Any:
        """
        Identifies the best-matching function, dynamically imports it,
        """
        function_name = self.find_best_function(user_input)
        return function_name  # ✅ Execute function with filled arguments
