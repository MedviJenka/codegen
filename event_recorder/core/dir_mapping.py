import os
import ast
from event_recorder.core.paths import GLOBAL_PATH


class FunctionDiscovery:

    def __init__(self) -> None:
        self.base_directory = GLOBAL_PATH
        self.functions_index = self._scan_directory()

    def _scan_directory(self) -> dict[str, dict[str, tuple[str, str]]]:
        """
        Scans the base directory for Python files, extracts function names and docstrings,
        and returns a dictionary mapping file names to their functions and docstrings.
        """
        files_functions = {}
        for root, _, files in os.walk(self.base_directory):
            if '.venv' in root or 'venv' in root:
                continue
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    module_name = os.path.splitext(os.path.relpath(file_path, self.base_directory))[0].replace(os.sep, ".")
                    extracted_functions = self._extract_functions(file_path, module_name)
                    files_functions[file_path] = extracted_functions
        return files_functions

    def _extract_functions(self, file_path: str, module_name: str) -> dict[str, tuple[str, str]]:
        """
        Extracts function names and their docstrings from a given Python file.
        """
        functions = {}
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""
                functions[node.name] = (module_name, docstring)
        return functions
