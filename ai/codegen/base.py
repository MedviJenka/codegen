from abc import ABC


class BiniBaseModel(ABC):

    def __init__(self, model: str, api_key: str, version: str, endpoint: str) -> None:
        self.model = model
        self.api_key = api_key
        self.version = version
        self.endpoint = endpoint
