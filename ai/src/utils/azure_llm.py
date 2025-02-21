import os
from crewai import LLM
from functools import cached_property
from openai import AzureOpenAI


class AzureLLMConfig:

    """class template to handle original .env bini config"""

    api_key: str = os.getenv("OPENAI_API_KEY")
    endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version: str = os.getenv("OPENAPI_API_VERSION")
    model: str = f'azure/{os.getenv("MODEL")}'
    temperature: float = 0.0

    @cached_property
    def llm(self) -> LLM:
        return LLM(
            model=self.model,
            base_url=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
            temperature=self.temperature
        )

    @cached_property
    def azure_llm(self) -> AzureOpenAI:
        return AzureOpenAI(api_key=self.api_key,
                           api_version=self.api_version,
                           azure_endpoint=self.endpoint)
