import os
from dataclasses import dataclass
from crewai import LLM
from functools import cached_property
from crewai.telemetry import Telemetry
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


load_dotenv()


class TelemetryPatch:

    def __init__(self) -> None:
        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, self.__noop)

    def __noop(*args: any, **kwargs: any) -> None:
        """dummy function for handling telemetry"""
        pass


class AzureLLMConfig(TelemetryPatch):

    api_key: str = os.getenv("AZURE_API_KEY")
    endpoint: str = os.getenv("AZURE_API_BASE")
    version: str = os.getenv("AZURE_API_VERSION")
    model: str = os.getenv("MODEL")

    def __post_init__(self) -> None:
        if not all([self.api_key, self.endpoint, self.version, self.model]):
            raise ValueError("Missing Azure OpenAI environment variables!")
        if self.api_key != 'OPENAI_API_KEY':
            self.api_key = os.getenv('OPENAI_API_KEY')

        super().__init__()

    @cached_property
    def llm(self) -> LLM:
        return LLM(model=self.model, api_version=self.version, temperature=0)

    @cached_property
    def langchain_llm(self) -> AzureChatOpenAI:
        """Fix LangChain API handling for Azure"""
        return AzureChatOpenAI(
            openai_api_type="azure",
            azure_endpoint=self.endpoint,
            openai_api_key=self.api_key,
            openai_api_version=self.version,
            deployment_name=self.model
        )
