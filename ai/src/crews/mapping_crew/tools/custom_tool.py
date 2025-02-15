import os
import ast
import hashlib
from typing import Any
import diskcache as dc
from src.core.paths import FUNCTIONS_INDEX


class FunctionMapping:

    def __init__(self, base_dir=FUNCTIONS_INDEX) -> None:
        self.base_dir = base_dir
        self.cache = dc.Cache(f"{base_dir}/func_cache_db")

    def extract_wildcard_cells(self):
        """Reads a file and extracts table cells that contain the '*' wildcard."""
        extracted_cells = []

        with open(self.base_dir, 'r', encoding='utf-8') as file:
            for line in file:
                cells = line.split('|')
                for cell in cells:
                    if '*' in cell:
                        extracted_cells.append(cell.strip().replace('*', '').strip())

        return extracted_cells

    @property
    def index_functions(self) -> dict:
        return self.scan_directory()

    def scan_directory(self) -> dict:
        """
        Scans the base directory for Python files, extracts function names and docstrings,
        and caches results to avoid redundant processing.
        """
        files_functions = {}
        for root, _, files in os.walk(self.base_dir):  # ✅ Use self.base_dir
            if '.venv' in root or 'venv' in root:
                continue
            for file in files:
                if file.endswith(".py"):
                    file_path: Any = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(file_path, self.base_dir))[0].replace(os.sep, ".")
                    extracted_functions = self.__extract_functions_with_cache(file_path, module_name)
                    files_functions[file_path] = extracted_functions
        return files_functions

    def __extract_functions_with_cache(self, file_path: list or str, module_name: str) -> dict[str, tuple[str, str]]:
        """Extracts function names and docstrings from a Python file, using caching to avoid redundant parsing."""
        last_modified = os.path.getmtime(file_path)  # ✅ Get last modified timestamp
        cache_key = self.__generate_cache_key(file_path)

        # ✅ Check if cached version exists and is up-to-date
        if cache_key in self.cache and self.cache[cache_key]['timestamp'] == last_modified:
            return self.cache[cache_key]['functions']

        # ✅ If not cached or outdated, parse the file and update cache
        functions = self.__extract_functions(file_path, module_name)
        self.cache[cache_key] = {'functions': functions, 'timestamp': last_modified}
        return functions

    @staticmethod
    def __extract_functions(file_path: str, module_name: str) -> dict:
        """
        Extracts function names and their docstrings from a given Python file.
        """
        functions = {}
        with open(file_path, "r", encoding="utf-8") as file:  # ✅ Read from file_path
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""
                functions[node.name] = (module_name, docstring)
        return functions

    @staticmethod
    def __generate_cache_key(file_path: str) -> str:
        """
        Generates a unique cache key based on the file path.
        """
        return hashlib.md5(file_path.encode()).hexdigest()
