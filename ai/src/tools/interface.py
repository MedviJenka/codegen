from pydantic import BaseModel, Field


class FunctionMapInterface(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="getting user input")
