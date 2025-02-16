from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
from ai.src.tools.functions import FunctionMapping
from ai.src.tools.interface import FunctionMapInterface
from src.core.paths import FUNCTIONS_INDEX


class FunctionMappingTool(BaseTool):

    name: str = "Function Mapping Tool"
    description: str = "getting the relevant functions"
    query: Type[BaseModel] = FunctionMapInterface
    # base_dir: str = FUNCTIONS_INDEX

    def _run(self, query: str) -> str:
        if isinstance(query, dict):  # Handle incorrect input type
            query.get("query", query)

        f = FunctionMapping()
        return f.get_all_mappings()


