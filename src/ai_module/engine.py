from crewai import Flow, Crew
from src.ai_module.agents import CustomAgents
from src.ai_module.tasks import BiniTasks
from src.ai_module.tools import ToolKit


class BiniCode:

    def __init__(self) -> None:
        self.__agent = CustomAgents()
        self.__tools = ToolKit()

    @property
    def __tasks(self) -> BiniTasks:
        return BiniTasks(toolkit=self.__tools)

    def test(self, path: str) -> None:
        """Executes the automated workflow"""
        test_plan_task = self.__tasks.view_test_plan(test_plan=path)
        tasks = [test_plan_task]
        crew = Crew(tasks=tasks)
        crew.kickoff()


bini = BiniCode()
bini.test(r'C:\Users\medvi\PycharmProjects\codegen\tests\test_plan.md')
