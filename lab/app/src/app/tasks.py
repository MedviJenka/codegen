import yaml
from crewai import Task
from crewai.project import task, CrewBase
from lab.app.src.app.agents import Agents
from lab.app.src.app.tools.toolkit import ToolKit


@CrewBase
class Tasks:

    """Manages all task configurations and creation."""

    def __init__(self) -> None:
        self.agents = Agents()
        with open("config/tasks.yaml", "r", encoding="utf-8") as file:
            self.tasks_config = yaml.safe_load(file)

    @property
    def toolkit(self) -> ToolKit:
        return ToolKit()

    @task
    def test_plan_task(self) -> Task:
        """Creates the test plan task with an assigned agent."""
        return Task(
            config=self.tasks_config['test_plan_task'],
        )

    @task
    def function_mapping_task(self) -> Task:
        """Creates the function mapping task with an assigned agent."""
        return Task(
            config=self.tasks_config['function_mapping_task'],
        )
