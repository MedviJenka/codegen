import urllib3
import requests
from crewai import Crew
from src.ai_module.agents import CustomAgents
from src.ai_module.tasks import BiniTasks
from src.ai_module.tools import ToolKit
from src.core.executor import Executor
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
        return BiniTasks(toolkit=self.__tools)

    def execute(self, event_list: list[str], original_code: str) -> None:

        """Executes the automated workflow"""

        test_plan_path = r'C:\Users\evgenyp\PycharmProjects\codegen\tests\test_plan.md'

        ai_page_base_task = self.__tasks.update_page_base_task(event_list=event_list,
                                                               page_base=r"C:\Users\evgenyp\PycharmProjects\codegen\src\output\page_base.csv")

        # Step 1: Generate test automation code based on the test plan
        pytest_task = self.__tasks.generate_test(test_plan=test_plan_path, original_code=original_code)

        # Step 2: Perform code review before security validation
        code_review_task = self.__tasks.code_review_task(original_code=str(pytest_task))

        # Step 3: Conduct a security check on the reviewed code
        security_check_task = self.__tasks.security_check_task(updated_code=str(code_review_task))

        # Step 4: Final code review
        post_review_task = self.__tasks.code_review_task(str(security_check_task))

        # Step 5: Generate code
        # python_file = r'C:\Users\evgenyp\PycharmProjects\codegen\src\browser_recorder'
        # generate_code_task = self.__tasks.python_task(file_path=python_file, content=str(post_review_task))

        tasks = [ai_page_base_task]

        crew = Crew(tasks=tasks)
        crew.kickoff()
