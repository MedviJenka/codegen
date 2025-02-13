import yaml
from crewai import Task
from crewai.project import task, CrewBase
from lab.app.src.app.agents import Agents


@CrewBase
class Tasks:
    """Manages all task configurations and creation."""

    def __init__(self):
        self.tasks = None
        self.agents = Agents()  # ✅ Initialize agents properly
        with open("config/tasks.yaml", "r", encoding="utf-8") as file:
            self.tasks_config = yaml.safe_load(file)

    @task
    def test_plan_task(self) -> Task:
        """Creates the test plan task with an assigned agent."""
        return Task(  # ✅ Call function to get the agent
            config=self.tasks_config['test_plan_task']
        )
