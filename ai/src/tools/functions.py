import os
import ast
import hashlib
import diskcache as db
import json
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
        """Scans Python files in base directory, extracts function and class definitions, and caches them."""
        files_content = {}
        for root, _, files in os.walk(self.base_dir):
            if '.venv' in root or 'venv' in root:
                continue
            for file in files:
                if file.endswith(".py"):
                    file_path: Any = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(file_path, self.base_dir))[0].replace(os.sep, ".")

                    extracted_content = self.__extract_content_with_cache(file_path, module_name)
                    if extracted_content:
                        files_content[module_name] = extracted_content
        return files_content

    def __extract_content_with_cache(self, file_path: str, module_name: str) -> Dict:
        """Extracts function and class details with caching."""
        last_modified = os.path.getmtime(file_path)
        cache_key = self.__generate_cache_key(file_path)

        if cache_key in self.cache and self.cache[cache_key]['timestamp'] == last_modified:
            return self.cache[cache_key]['content']

        content = self.__extract_content(file_path, module_name)
        self.cache[cache_key] = {'content': content, 'timestamp': last_modified}
        return content

    @staticmethod
    def __extract_content(file_path: str, module_name: str) -> dict:
        """Extracts function names, their docstrings, argument names, and types from a Python file."""
        content = {"functions": {}, "classes": {}}
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        class_parents = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_parents[node] = node.body  # Store class bodies

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if any(node in body for body in class_parents.values()):
                    continue  # Skip class methods and __init__
                docstring = ast.get_docstring(node) or ""
                args = {
                    arg.arg: arg.annotation.id if isinstance(arg.annotation, ast.Name) else "Unknown"
                    for arg in node.args.args if arg.arg != "self"
                }

                content["functions"][node.name] = {"module": module_name, "docstring": docstring, "arguments": args}

            elif isinstance(node, ast.ClassDef):
                class_docstring = ast.get_docstring(node) or ""
                class_data = {"docstring": class_docstring, "init_args": {}, "methods": {}}

                for sub_node in node.body:
                    if isinstance(sub_node, ast.FunctionDef) and sub_node.name == "__init__":
                        class_data["init_args"] = {
                            arg.arg: arg.annotation.id if isinstance(arg.annotation, ast.Name) else "Unknown"
                            for arg in sub_node.args.args if arg.arg != "self"
                        }
                    elif isinstance(sub_node, ast.FunctionDef):
                        method_docstring = ast.get_docstring(sub_node) or ""
                        method_args = {
                            arg.arg: arg.annotation.id if isinstance(arg.annotation, ast.Name) else "Unknown"
                            for arg in sub_node.args.args if arg.arg != "self"
                        }
                        class_data["methods"][sub_node.name] = {"docstring": method_docstring, "arguments": method_args}

                content["classes"][node.name] = class_data

        return content

    @staticmethod
    def __generate_cache_key(file_path: str) -> str:
        """Generates a unique cache key based on the file path."""
        return hashlib.md5(file_path.encode()).hexdigest()

    def get_all_mappings(self) -> str:
        """Returns a JSON string of all functions and classes mapped to their details."""
        mappings = {"functions": {}, "classes": {}}
        for module, content in self.index_functions.items():
            for fn, data in content["functions"].items():
                mappings["functions"][fn] = data
            for cls, data in content["classes"].items():
                mappings["classes"][cls] = data
        return json.dumps(mappings, indent=4)

