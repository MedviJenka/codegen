import requests
from textwrap import dedent
from crewai import Agent
from bini_ai.core.modules.environment import get_dotenv_data
from bini_ai.engine.azure_config import AzureOpenAIConfig
from bini_ai.engine.base_model import BiniBaseModel
from bini_ai.engine.request_handler import APIRequestHandler
from bini_ai.infrastructure.constants import IMAGE_1
from bini_ai.infrastructure.enums import Prompts


class CustomAgents:

    def __init__(self) -> None:
        self.config = AzureOpenAIConfig()

    def memory_agent(self):
        return Agent(
            role='Research Specialist',
            goal='Conduct thorough research on people and companies involved in the meeting',
            backstory=dedent("""\
                    As a Research Specialist, your mission is to uncover detailed information
                    about the individuals and entities participating in the meeting. Your insights
                    will lay the groundwork for strategic meeting preparation."""),
            verbose=True,
            llm=self.config.set_azure_llm
        )


class BiniCode(BiniBaseModel, APIRequestHandler):
    """
    A class to manage interactions with the Bini OpenAI deployment.
    :param: model The model name for the OpenAI deployment.
    :param: api_key (str): The API key for accessing the OpenAI service.
    :param: version (str): The version of the OpenAI API to use.
    :param: endpoint (str): final azure openai endpoint

    """

    def __init__(self, model: str, version: str, endpoint: str, api_key: str) -> None:
        self.__set_agent = CustomAgents()
        self.session = requests.Session()
        BiniBaseModel.__init__(self, model=model, version=version, endpoint=endpoint, api_key=api_key)

    def memory_agent(self) -> callable:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.memory_agent()

    def format_agent_prompt(self):
        """Converts the agent object into a formatted string for GPT-4."""
        agent = self.memory_agent()
        return f"""
            Role: {agent.role}
            Goal: {agent.goal}
            Backstory: {agent.backstory}
		"""

    def run_image_processing(self, image_path: str) -> str:
        """
		Sends request to the image visualization engine.
		If self.sample_image is provided, it will include the sample image in the payload.
		:return: Image processing output as a string.

		"""

        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
            {"type": "text", "text": self.format_agent_prompt()}  # self.prompt for prompt without agent
        ]

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_visualization_prompt}]},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0,
        }

        return self.make_request_with_retry(payload=payload)


class BiniUtils(BiniCode):
    """
    A utility class for interacting with the OpenAI API using Azure's infrastructure.

    This class extends the `Bini` class and initializes the necessary attributes such as
    the model, API key, API version, and endpoint by retrieving these values from environment
    variables.

    Attributes:
        model (str): The model to be used with the OpenAI API, retrieved from environment variables.
        api_key (str): The API key for authenticating requests to the OpenAI API, retrieved from environment variables.
        version (str): The version of the OpenAI API to be used, retrieved from environment variables.
        endpoint (str): The Azure endpoint for the OpenAI API, retrieved from environment variables.

    Methods:
        __init__: Initializes the IRBiniUtils class by setting up the model, API key, version, and endpoint.

    """

    def __init__(self) -> None:
        self.model: str = get_dotenv_data('MODEL')
        self.api_key: str = get_dotenv_data('OPENAI_API_KEY')
        self.version: str = get_dotenv_data('OPENAI_API_VERSION')
        self.endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')
        super().__init__(endpoint=self.endpoint, model=self.model, version=self.version, api_key=self.api_key)


bini = BiniUtils()
print(bini.run_image_processing(image_path=IMAGE_1))
