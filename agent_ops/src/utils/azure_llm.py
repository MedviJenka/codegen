import os
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
                setattr(Telemetry, attr, self.__nop)

    def __nop(*args: any, **kwargs: any) -> None:
        """NOT OPERATIVE function for handling telemetry"""
        pass


class AzureLLMConfig(TelemetryPatch):

    model: str = os.getenv("MODEL")
    api_key: str = os.getenv("AZURE_API_KEY")
    endpoint: str = os.getenv("AZURE_API_BASE")
    version: str = os.getenv("AZURE_API_VERSION")

    temperature: float = 0.1

    def __post_init__(self) -> None:
        super().__init__()
        if not all([self.api_key, self.endpoint, self.version, self.model]):
            raise ValueError("Missing Azure OpenAI environment variables!")

    @cached_property
    def llm(self) -> LLM:
        return LLM(model=self.model,
                   api_version=self.version,
                   api_key=self.api_key,
                   api_base=self.endpoint,
                   temperature=self.temperature)

    @cached_property
    def azure_openai_llm(self) -> AzureChatOpenAI:
        # Map the existing environment variables to the required Azure OpenAI keys
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_API_KEY")
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_API_BASE")
        os.environ["OPENAI_API_VERSION"] = os.getenv("AZURE_API_VERSION")

        if not all([os.environ["AZURE_OPENAI_API_KEY"],
                    os.environ["AZURE_OPENAI_ENDPOINT"],
                    os.environ["OPENAI_API_VERSION"]]):
            raise ValueError("Missing required Azure OpenAI environment variables!")

        return AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
            openai_api_version=os.environ["OPENAI_API_VERSION"],
            deployment_name=self.model
        )
