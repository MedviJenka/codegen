from src.core.executor import Executor
from crewai import Agent, Task, Crew
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool, FileReadTool


@CrewBase
class CrewBlueprint(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def agent(self) -> Agent:
        read_tool = FileReadTool(filename=__name__)
        write_tool = FileWriterTool(filename=__name__)
        return Agent(config=self.agents_config['debug_agent'],
                     verbose=True,
                     llm=self.llm,
                     tools=[read_tool, write_tool])

    @task
    def task(self) -> Task:
        return Task(config=self.tasks_config['debug_task'])

    @crew
    def crew(self) -> Crew:
        return Crew()

    def execute(self, error_details: str, original_code: str) -> str:
        self.crew().kickoff(inputs={})

