import urllib3
import requests
from typing import Optional
from crewai import Crew
from crewai.crews import CrewOutput
from src.ai_module.agents import CustomAgents
from src.ai_module.tasks import BiniTasks
from src.ai_module.tools import ToolKit
from src.core.executor import Executor
from src.core.paths import IMAGE_2
from src.infrastructure.enums import Prompts
from src.utils.base import BiniBaseModel
from src.utils.request_handler import APIRequestHandler


urllib3.disable_warnings()


class BiniCode(APIRequestHandler, BiniBaseModel, Executor):

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

    def execute(self, event_list: list[str], based_on: Optional[str] = IMAGE_2) -> CrewOutput:
        # Step 1: Extract UI elements
        elements = self.run_image_processing(image_path=based_on)

        # Step 2: Create a test plan using extracted UI elements
        test_plan_task = self.__tasks.create_test_plan(ui_elements=elements)

        # Step 3: Map UI elements into a structured format for testing
        map_elements_task = self.__tasks.map_elements_task(event_list=event_list)

        # Step 4: Generate test automation code from the test plan
        pytest_task = self.__tasks.generate_pytest_code(test_plan=test_plan_task)

        # Step 5: Perform code review on the generated test code
        code_review_task = self.__tasks.code_review_task

        # Step 6: Conduct a security check on the test scripts
        security_check_task = self.__tasks.security_check

        # Execute CrewAI workflow with linked tasks
        crew = Crew(
            agents=[
                self.__agent.memory_agent(),
                self.__agent.map_elements_agent(),
                self.__agent.code_agent(),
                self.__agent.security_agent()
            ],
            tasks=[
                map_elements_task,   # Runs first (maps elements)
                test_plan_task,      # Uses mapped elements to create a test plan
                pytest_task,         # Uses the test plan to generate test scripts
                code_review_task,    # Reviews the generated test scripts
                security_check_task  # Performs a security review on the scripts
            ]
        )

        result = crew.kickoff()
        return result
