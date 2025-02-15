from ai.src.crews.test_plan_crew.tools.custom_tool import FunctionMapping


class ToolKit(FunctionMapping):

    @staticmethod
    def read_test_plan(path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
