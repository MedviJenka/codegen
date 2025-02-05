import requests
from typing import Optional
from crewai import Crew
from ai.codegen.agents import CustomAgents
from ai.codegen.base import BiniBaseModel
from ai.codegen.request_handler import APIRequestHandler
from ai.codegen.tasks import BiniTasks
from ai.codegen.tools import ToolKit
from ai.infrastructure.constants import IMAGE_2
from ai.infrastructure.enums import Prompts
import urllib3

urllib3.disable_warnings()


class BiniCode(APIRequestHandler, BiniBaseModel):

    def __init__(self, model: str, version: str, endpoint: str, api_key: str) -> None:
        self.__agent = CustomAgents()
        self.__tools = ToolKit()
        self.session = requests.Session()
        BiniBaseModel.__init__(self, model=model, version=version, endpoint=endpoint, api_key=api_key)

    @property
    def __tasks(self) -> BiniTasks:
        return BiniTasks(agent=self.__agent, toolkit=self.__tools)

    @property
    def screen_map_agent(self) -> str:
        agent = self.__agent.memory_agent()
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

    def execute_crew(self, based_on: Optional[str] = IMAGE_2):

        # Step 1:
        elements = self.run_image_processing(image_path=based_on)

        # Step 2:
        test_plan = self.__tasks.create_test_plan(ui_elements=elements),

        # Execute CrewAI workflow
        crew = Crew(agents=[self.__agent.memory_agent(),
                            self.__agent.code_agent(),
                            self.__agent.security_agent(),
                            self.__agent.map_elements_agent()],
                    tasks=[self.__tasks.generate_pytest_code(test_plan=test_plan),
                           self.__tasks.code_review_task,
                           self.__tasks.security_check])

        result = crew.kickoff()
        return result
