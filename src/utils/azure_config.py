import os
from dataclasses import dataclass
from functools import cached_property
from langchain_openai import AzureChatOpenAI
from src.environment.environment import get_dotenv_data
from src.utils.base import BiniBaseModel


@dataclass
class AzureOpenAIConfig(BiniBaseModel):

    model: str = os.getenv('MODEL')
    api_key: str = os.getenv('OPENAI_API_KEY')
    version: str = os.getenv('AZURE_API_VERSION')
    endpoint: str = os.getenv('AZURE_API_BASE')

    @cached_property
    def set_azure_llm(self) -> AzureChatOpenAI:

        """Initiates openai with azure"""

        return AzureChatOpenAI(
            deployment_name=self.model,
            openai_api_version=self.version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key)
