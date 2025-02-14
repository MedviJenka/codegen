import os
from functools import cached_property
from crewai import Crew, Process, Task, LLM
from crewai.project import CrewBase, crew, task

from lab.app.src.app.agents import Agents
from lab.app.src.app.tasks import Tasks
from lab.app.src.app.tools.toolkit import ToolKit
from src.core.paths import TEST_PLAN


@CrewBase
class App(Agents, Tasks):

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.test_agent()],  # ✅ Ensure the agent is instantiated properly
            tasks=[self.test_plan_task()],  # ✅ Call the method properly
            process=Process.sequential,
            verbose=True
        )


toolkit = ToolKit()
app = App()
app.crew().kickoff(inputs={'test_plan': toolkit.read_test_plan(path=TEST_PLAN)})
