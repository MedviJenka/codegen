from abc import ABC, abstractmethod
from crewai import Agent, Crew, Process, Task
from crewai.crews import CrewOutput
from crewai.project import CrewBase, agent, crew, task
from lab.src.azure_llm import AzureLLMConfig
from typing import Optional
from lab.src.crews.mapping_crew.tools.toolkit import ToolKit


class Executor(ABC):

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> None:
        pass


@CrewBase
class MappingCrew(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def code_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_agent'],
            verbose=True,
            llm=self.llm
        )

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config['code_task'])

    @crew
    def map_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def execute(self, functions: any) -> list[CrewOutput]:
        tool = ToolKit()
        data = [{'tool': str(tool.index_functions)}]
        return self.map_crew().kickoff_for_each(inputs=data)
