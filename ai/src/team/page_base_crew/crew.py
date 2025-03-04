from crewai.crews import CrewOutput
from src.core.paths import PAGE_BASE
from src.core.executor import Executor
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool


@CrewBase
class CSVCrew(AzureLLMConfig, Executor):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def csv_agent(self) -> Agent:

        return Agent(config=self.agents_config['csv_agent'],
                     verbose=True,
                     llm=self.llm,
                     max_retry_limit=3,
                     tools=[FileReadTool(file_path=PAGE_BASE),
                            FileWriterTool(filename=PAGE_BASE, overwrite=True)])

    @task
    def csv_task(self) -> Task:
        return Task(config=self.tasks_config['csv_task'])

    @crew
    def csv_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self) -> CrewOutput:
        return self.csv_crew().kickoff()
