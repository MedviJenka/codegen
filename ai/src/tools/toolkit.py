from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
from ai.src.tools.functions import FunctionMapping
from ai.src.tools.interface import FunctionMapInterface, ReadTestPlanToolInterface
from src.core.paths import TEST_PLAN


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
