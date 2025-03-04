from ai.src.utils.azure_llm import AzureLLMConfig


class TestAzureConfig:

    def test_azure_api_connection(self) -> None:
        azure = AzureLLMConfig()
        assert '0fb0' in azure.api_key
        assert 'azure/' in azure.model
