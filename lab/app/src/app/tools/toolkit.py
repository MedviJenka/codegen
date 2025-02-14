from lab.app.src.app.tools.custom_tool import FunctionMapping


class ToolKit(FunctionMapping):

    @staticmethod
    def read_test_plan(path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def find_relevant_functions(self) -> dict:
        """returns full dict with function paths, name and docstring"""
        return self.index_functions
