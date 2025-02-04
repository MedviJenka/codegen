from enum import StrEnum
from ai.infrastructure.prompts import IMAGE_VISUALIZATION_PROMPT


class Prompts(StrEnum):

    image_visualization_prompt: str = IMAGE_VISUALIZATION_PROMPT
    element_memory_prompt: str = """map all the elements you see in this screenshot, such as buttons fields etc map then as json structure. these elements will be used to create a test plan"""
    test_plan_prompt: str = ''
    code_expert_prompt: str = ''
