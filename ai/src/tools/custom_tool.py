import os
import ast
import hashlib
import importlib
import inspect
from typing import Any, Dict, Tuple
import diskcache as db
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
                    file_path = os.path.join(root, file)
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

    def __extract_functions(self, file_path: str, module_name: str) -> Dict[str, Tuple[str, str]]:
        """Extracts function names and their docstrings from a Python file."""
        functions = {}
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""
                functions[node.name] = (module_name, docstring)
        return functions

    def __generate_cache_key(self, file_path: str) -> str:
        """Generates a unique cache key based on the file path."""
        return hashlib.md5(file_path.encode()).hexdigest()

    def find_best_function(self, user_input: str) -> str:
        """
        Uses CrewAI agent to match user input to the most relevant function.
        """
        function_index = {fn: doc for module in self.index_functions.values() for fn, (_, doc) in module.items()}

        # ✅ Pass function_index with a strict prompt
        response = self.client.execute(
            user_input=user_input,
            function_index=function_index
        )

        # ✅ Debug CrewOutput structure
        if isinstance(response, CrewOutput):
            print(f"DEBUG: CrewOutput contents -> {response}")
            function_name = str(response).strip()  # Convert CrewOutput to string
        elif isinstance(response, list) and response:
            function_name = str(response[0]).strip()  # Convert first list item to a string
        elif isinstance(response, str):
            function_name = response.strip()
        else:
            return "Error: AI did not return a valid function name"

        # ✅ Ensure function_name exists in function_index
        if function_name not in function_index:
            print(f"ERROR: AI selected function '{function_name}' that does not exist.")
            return "Error: Selected function does not exist"

        return function_name

    def execute_function(self, user_input: str, **kwargs) -> Any:
        """
        Identifies the best-matching function, dynamically imports it, and executes it with arguments.
        """
        function_name = self.find_best_function(user_input)

        # ✅ Find the corresponding module
        module_name = None
        for mod_name, functions in self.index_functions.items():
            if function_name in functions:
                module_name = mod_name
                break

        if not module_name:
            return f"No matching function found for '{user_input}'."

        # ✅ Convert module_name to a correct Python import format
        module_name = f"functions.{module_name}"

        # ✅ Dynamically import and execute the function
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)

            # ✅ Inspect function signature to determine required arguments
            signature = inspect.signature(function)
            required_args = {
                param: kwargs.get(param) for param in signature.parameters if param in kwargs
            }

            return function(**required_args)  # ✅ Execute function with matched arguments
        except (ModuleNotFoundError, AttributeError, TypeError) as e:
            return f"Error executing function '{function_name}': {str(e)}"


# ✅ Try Running Again
f = FunctionMapping()
print(f.execute_function('* create call with 2 users'))




# import os
# import ast
# import hashlib
# from typing import Any
# import diskcache as db
# from src.core.paths import FUNCTIONS_INDEX
# from typing import Type
# from crewai.tools import BaseTool
# from pydantic import BaseModel, Field
#
#
# class ToolKitBase(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")
#
#
# class ToolKitInterface(BaseTool):
#
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#
#     args_schema: Type[BaseModel] = ToolKitBase
#
#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."
#
#
# class FunctionMapping:
#
#     def __init__(self, base_dir=FUNCTIONS_INDEX) -> None:
#         self.cache = db.Cache(f"{base_dir}/func_cache_db")
#         self.base_dir = base_dir
#
#     @property
#     def index_functions(self) -> dict:
#         return self.scan_directory()
#
#     def scan_directory(self) -> dict:
#         """
#         Scans the base directory for Python files, extracts function names and docstrings,
#         and caches results to avoid redundant processing.
#         """
#         files_functions = {}
#         for root, _, files in os.walk(self.base_dir):  # ✅ Use self.base_dir
#             if '.venv' in root or 'venv' in root:
#                 continue
#             for file in files:
#                 if file.endswith(".py"):
#                     file_path: Any = os.path.join(root, file)
#                     module_name = os.path.splitext(os.path.relpath(file_path, self.base_dir))[0].replace(os.sep, ".")
#                     extracted_functions = self.__extract_functions_with_cache(file_path, module_name)
#                     files_functions[file_path] = extracted_functions
#         return files_functions
#
#     def __extract_functions_with_cache(self, file_path: list or str, module_name: str) -> dict[str, tuple[str, str]]:
#         """Extracts function names and docstrings from a Python file, using caching to avoid redundant parsing."""
#         last_modified = os.path.getmtime(file_path)  # ✅ Get last modified timestamp
#         cache_key = self.__generate_cache_key(file_path)
#
#         # ✅ Check if cached version exists and is up-to-date
#         if cache_key in self.cache and self.cache[cache_key]['timestamp'] == last_modified:
#             return self.cache[cache_key]['functions']
#
#         # ✅ If not cached or outdated, parse the file and update cache
#         functions = self.__extract_functions(file_path, module_name)
#         self.cache[cache_key] = {'functions': functions, 'timestamp': last_modified}
#         return functions
#
#     @staticmethod
#     def __extract_functions(file_path: str, module_name: str) -> dict:
#         """
#         Extracts function names and their docstrings from a given Python file.
#         """
#         functions = {}
#         with open(file_path, "r", encoding="utf-8") as file:  # ✅ Read from file_path
#             tree = ast.parse(file.read())
#
#         for node in ast.walk(tree):
#             if isinstance(node, ast.FunctionDef):
#                 docstring = ast.get_docstring(node) or ""
#                 functions[node.name] = (module_name, docstring)
#         return functions
#
#     @staticmethod
#     def __generate_cache_key(file_path: str) -> str:
#         """
#         Generates a unique cache key based on the file path.
#         """
#         return hashlib.md5(file_path.encode()).hexdigest()
