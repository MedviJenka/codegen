from dataclasses import dataclass
from functools import cached_property
from langchain_openai import AzureChatOpenAI
from src.environment.environment import get_dotenv_data


@dataclass
class AzureOpenAIConfig:
    """
    A configuration class to manage environment settings for Azure OpenAI deployment.
    """
    api_key: str = get_dotenv_data('OPENAI_API_KEY')
    model: str = get_dotenv_data('MODEL')
    openai_api_version: str = get_dotenv_data('OPENAI_API_VERSION')
    azure_endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')

    @cached_property
    def set_azure_llm(self) -> AzureChatOpenAI:

        """Initiates openai with azure"""

        return AzureChatOpenAI(
            deployment_name=self.model,
            openai_api_version=self.openai_api_version,
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key
        )
