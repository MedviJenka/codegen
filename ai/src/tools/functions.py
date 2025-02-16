import os
import ast
import hashlib
import diskcache as db
from typing import Any, Dict, Tuple, List
from src.core.paths import FUNCTIONS_INDEX


class FunctionMapping:

    def __init__(self, base_dir=FUNCTIONS_INDEX) -> None:
        self.cache = db.Cache(f"{base_dir}/func_cache_db")
        self.base_dir = base_dir

    @property
    def index_functions(self) -> Dict[str, Dict[str, Tuple[str, str, List[str]]]]:
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
                    if extracted_functions:
                        files_functions[module_name] = extracted_functions
        return files_functions

    def __extract_functions_with_cache(self, file_path: str, module_name: str) -> Dict:
        """Extracts function names, arguments, and docstrings with caching."""
        last_modified = os.path.getmtime(file_path)
        cache_key = self.__generate_cache_key(file_path)

        if cache_key in self.cache and self.cache[cache_key]['timestamp'] == last_modified:
            return self.cache[cache_key]['functions']

        functions = self.__extract_functions(file_path, module_name)
        self.cache[cache_key] = {'functions': functions, 'timestamp': last_modified}
        return functions

    @staticmethod
    def __extract_functions(file_path: str, module_name: str) -> dict:
        """Extracts function names, their docstrings, and arguments from a Python file."""
        functions = {}
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""

                # Extract function arguments properly
                args = [arg.arg for arg in node.args.args or node.args.kwonlyargs]  # Positional arguments
                args += [arg.arg for arg in node.args.kwonlyargs]  # Keyword-only arguments

                if node.args.vararg:  # *args
                    args.append(f"*{node.args.vararg.arg}")

                if node.args.kwarg:  # **kwargs
                    args.append(f"**{node.args.kwarg.arg}")

                # Ensure args is a flat list
                functions[node.name] = [module_name, docstring, args]

        return functions

    @staticmethod
    def __generate_cache_key(file_path: str) -> str:
        """Generates a unique cache key based on the file path."""
        return hashlib.md5(file_path.encode()).hexdigest()

    def get_all_functions(self) -> dict:
        """Returns a dictionary of all functions mapped to their module, docstring, and arguments."""
        function_index = {
            fn: (module, doc, args if isinstance(args, list) else [])  # Ensure args is always a list
            for module in self.index_functions.values()
            for fn, data in module.items()
            for module, doc, *args in [data]  # Unpack safely
        }
        return function_index


# Instantiate and print function mappings
# print(f.get_all_functions())
f = FunctionMapping()
f.cache.clear()
print(f.get_all_functions())
