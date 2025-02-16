from pydantic import BaseModel, Field


class FunctionMapInterface(BaseModel):
    """Input schema for MyCustomTool."""
    user_input: str = Field(..., description="getting user input")
