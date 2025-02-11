from abc import ABC


class BiniBaseModel(ABC):

    def __init__(self, api_key: str, model: str, version: str, endpoint: str) -> None:
        self.api_key = api_key
        self.model = model
        self.version = version
        self.endpoint = f"{endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"
