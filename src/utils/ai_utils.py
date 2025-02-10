from src.ai_module.engine import BiniCode
from src.utils.azure_config import AzureOpenAIConfig


class BiniCodeUtils(BiniCode):

    def __init__(self) -> None:

        config = AzureOpenAIConfig()
        super().__init__(
            endpoint=config.azure_endpoint,
            model=config.model,
            version=config.openai_api_version,
            api_key=config.api_key
        )
