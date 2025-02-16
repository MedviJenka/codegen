from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
from ai.src.tools.functions import FunctionMapping
from ai.src.tools.interface import FunctionMapInterface


class FunctionMappingTool(BaseTool, FunctionMapping):

    name: str = "Function Mapping Tool"
    description: str = "getting the relevant functions"
    args_schema: Type[BaseModel] = FunctionMapInterface

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

    def execute(self, user_input: str) -> None:
        self.execute_function(user_input=user_input)
