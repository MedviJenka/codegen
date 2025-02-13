import os
import yaml
from functools import cached_property
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from lab.app.src.app.agents import Agents
from lab.app.src.app.tasks import Tasks


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class App(Agents, Tasks):

    @cached_property
    def llm(self) -> LLM:
        return LLM(model=os.getenv('MODEL'), api_version=os.getenv('AZURE_API_VERSION'))

    @task
    def test_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_plan_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )


app = App()
app.crew().kickoff()
