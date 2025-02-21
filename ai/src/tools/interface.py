from pydantic import BaseModel, Field


class FunctionMapInterface(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="getting user input")


class ReadTestPlanToolInterface(BaseModel):
    """Input schema for MyCustomTool."""
    test_plan: str = Field(..., description="getting user input")


class ImageVisionToolInterface(BaseModel):
    """Input schema for MyCustomTool."""
    image_path: str = Field(..., description="The image path")
