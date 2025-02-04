import requests
from crewai import Crew
from bini_ai.engine.base_model import BiniBaseModel
from bini_ai.engine.request_handler import APIRequestHandler
from bini_ai.infrastructure.constants import IMAGE_1
from bini_ai.infrastructure.enums import Prompts
from bini_code.agents import CustomAgents
from bini_code.tasks import AgentTasks


class BiniCode(BiniBaseModel, APIRequestHandler):

    def __init__(self, model: str, version: str, endpoint: str, api_key: str) -> None:
        self.__set_agent = CustomAgents()
        self.__set_tasks = AgentTasks(self.__set_agent.memory_agent())
        self.session = requests.Session()
        BiniBaseModel.__init__(self, model=model, version=version, endpoint=endpoint, api_key=api_key)

    @property
    def screen_map_agent(self) -> str:
        agent = self.__set_agent.memory_agent()
        return f"Role: {agent.role} Goal: {agent.goal} Backstory: {agent.backstory}"

    def run_image_processing(self, image_path: str) -> str:
        """Extracts UI elements from an image and returns structured JSON"""

        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
            {"type": "text", "text": self.screen_map_agent},
        ]

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_visualization_prompt}]},
                {"role": "user", "content": user_content},
            ],
            "temperature": 0,
        }

        response = self.make_request_with_retry(payload=payload)
        return response

    def execute_crew(self, device: str, based_on: str):

        # Step 1:
        ui_elements = self.run_image_processing(image_path=based_on)  # Provide your image path

        # Step 2: Generate a test plan based on UI elements
        test_plan_task = self.__set_tasks.create_test_plan(ui_elements=ui_elements)

        # Step 3: Generate Pytest Code from the test plan
        pytest_task = self.__set_tasks.generate_pytest_code(device=device, test_plan="Test plan details here")

        # Execute CrewAI workflow
        crew = Crew(agents=[self.__set_agent.memory_agent()], tasks=[test_plan_task, pytest_task])

        result = crew.kickoff()
        return result
