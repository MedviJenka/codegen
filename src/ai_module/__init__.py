import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


load_dotenv()


class AzureOpenAIConfig:
    def __init__(self) -> None:
        self.api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.version: str = os.getenv("AZURE_API_VERSION")
        self.model: str = os.getenv("MODEL")

        if not all([self.api_key, self.endpoint, self.version, self.model]):
            raise ValueError("Missing Azure OpenAI environment variables!")

    def get_langchain_llm(self) -> AzureChatOpenAI:
        """Fix LangChain API handling for Azure"""
        return AzureChatOpenAI(
            openai_api_type="azure",
            azure_endpoint=self.endpoint,
            openai_api_key=self.api_key,
            openai_api_version=self.version,
            deployment_name=self.model  # Use correct deployment name
        )
