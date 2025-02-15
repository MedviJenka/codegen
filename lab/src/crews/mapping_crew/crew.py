from abc import ABC, abstractmethod
from crewai import Agent, Crew, Process, Task
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
    def function_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['function_agent'],
            verbose=True,
            llm=self.llm
        )

    @task
    def function_task(self) -> Task:
        return Task(config=self.tasks_config['function_task'])

    @crew
    def map_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def execute(self) -> None:
        tool = ToolKit()
        data = [
            {
                'tool': str(tool.index_functions),
                'get_function': 'start a call with 2 users'
            }
        ]
        self.map_crew().kickoff_for_each(inputs=data)


m = MappingCrew()
m.execute()
