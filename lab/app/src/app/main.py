import os
from functools import cached_property
from crewai import Crew, Process, Task, LLM
from crewai.project import CrewBase, crew, task

from lab.app.src.app.agents import Agents
from lab.app.src.app.tasks import Tasks


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


app = App()
app.crew().kickoff()
