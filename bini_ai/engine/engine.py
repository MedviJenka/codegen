import requests
from typing import Optional
from bini_ai.core.agents.prompt_agent import SetAgent
from bini_ai.engine.base_model import BiniBaseModel
from bini_ai.engine.request_handler import APIRequestHandler
from bini_ai.infrastructure.common import format_friendly_message
from bini_ai.infrastructure.enums import Prompts


class Bini(BiniBaseModel, APIRequestHandler):

    """
    A class to manage interactions with the Bini OpenAI deployment.
    :param: model The model name for the OpenAI deployment.
    :param: api_key (str): The API key for accessing the OpenAI service.
    :param: version (str): The version of the OpenAI API to use.
    :param: endpoint (str): final azure openai endpoint

    """

    def __init__(self, model: str, version: str, endpoint: str, api_key: str) -> None:
        self.__set_agent = SetAgent()
        self.session = requests.Session()
        BiniBaseModel.__init__(self, model=model, version=version, endpoint=endpoint, api_key=api_key)

    def prompt_agent(self, result: str) -> callable:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.prompt_agent(result)

    def memory_agent(self, result: str) -> callable:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.set_memory_agent(result)

    def run_image_processing(self, image_path: str, prompt: str) -> str:

        """
        Sends request to the image visualization engine.
        If self.sample_image is provided, it will include the sample image in the payload.
        :return: Image processing output as a string.

        """

        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
            {"type": "text", "text": self.memory_agent(result=prompt)}  # self.prompt for prompt without agent
        ]

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_visualization_prompt}]},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0,
        }

        return self.make_request_with_retry(payload=payload)

    # def run(self, image_path: str or callable, prompt: str, task: Optional[str] = '', sample_image: Optional[str] = '') -> str:
    #
    #     """
    #     Runs Bini module using image path and sample image as an optional reference
    #
    #     previous result version, maybe will be rolled back in the future if needed.
    #
    #     """
    #
    #     try:
    #         result = self.run_image_processing(image_path=image_path, sample_image=sample_image, prompt=prompt, task=task)
    #         format_friendly_message(output=result, version=self.version, model=self.model, tokens=self.get_tokens())
    #         return result
    #
    #     except FileNotFoundError as e:
    #         raise f'⚠ File: {image_path} cannot be found, exception: {e} ⚠'
    #
    #     except requests.RequestException as e:
    #         raise f'⚠ Failed to send rest request, status code: {e} ⚠'
    #
