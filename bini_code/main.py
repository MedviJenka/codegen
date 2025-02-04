from bini_ai.infrastructure.constants import IMAGE_2
from bini_code.engine import BiniCode
from bini_ai.core.modules.environment import get_dotenv_data


class BiniUtils(BiniCode):

    def __init__(self) -> None:
        self.model: str = get_dotenv_data("MODEL")
        self.api_key: str = get_dotenv_data("OPENAI_API_KEY")
        self.version: str = get_dotenv_data("OPENAI_API_VERSION")
        self.endpoint: str = get_dotenv_data("AZURE_OPENAI_ENDPOINT")
        super().__init__(endpoint=self.endpoint, model=self.model, version=self.version, api_key=self.api_key)


if __name__ == '__main__':
    bini = BiniUtils()
    bini.execute_crew(device='mi', based_on=IMAGE_2)
