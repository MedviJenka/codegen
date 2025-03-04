from typing import Optional

from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.docx_search_tool.docx_search_tool import DOCXSearchTool


@CrewBase
class DOCXTeam(AzureLLMConfig, Executor):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def docx_agent(self) -> Agent:
        return Agent(config=self.agents_config['docx_agent'],
                     verbose=True,
                     tools=[DOCXSearchTool(docx='./file.docx')],
                     llm=self.llm)

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


DOCXTeam().execute(inputs='whats the name?')
