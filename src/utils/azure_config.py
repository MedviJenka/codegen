import os
from crewai import LLM
from functools import cached_property


class AzureOpenAIConfig:

    @cached_property
    def llm(self) -> LLM:
        return LLM(model=os.getenv('MODEL'), api_version=os.getenv('AZURE_API_VERSION'))
