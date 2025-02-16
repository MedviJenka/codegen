from ai.src.tools.functions import FunctionMapping


class ToolKit(FunctionMapping):

    @staticmethod
    def read_test_plan(path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
