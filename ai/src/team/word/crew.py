import os
from typing import Optional
from dotenv import load_dotenv
from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai_tools import DOCXSearchTool
from crewai.project import CrewBase, agent, crew, task


load_dotenv()
FILE = r'./file.docx'


@CrewBase
class MicrosoftWordAgent(Executor, AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def docx_agent(self) -> Agent:
        return Agent(config=self.agents_config['docx_agent'],
                     verbose=True,
                     llm=self.llm,
                     tools=[DOCXSearchTool(docx=FILE)])

    @task
    def docx_task(self) -> Task:
        return Task(config=self.tasks_config['docx_task'])

    @crew
    def docx_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self, inputs: str, raw_output: Optional[str] = False) -> CrewOutput or str:
        match raw_output:
            case True:
                return self.docx_crew().kickoff({'input': inputs}).raw
            case _:
                return self.docx_crew().kickoff({'input': inputs})


m = MicrosoftWordAgent()
m.execute(inputs='whats the name?')
