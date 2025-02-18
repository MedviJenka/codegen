from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from src.core.paths import PAGE_BASE, AI_PAGE_BASE


@CrewBase
class CSVCrew(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def csv_agent(self) -> Agent:

        return Agent(config=self.agents_config['csv_agent'],
                     verbose=True,
                     llm=self.llm,
                     tools=[
                         FileReadTool(file_path=PAGE_BASE),
                         FileWriterTool(filename=f'{AI_PAGE_BASE}')],
                     )

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


# app = CSVCrew()
# app.execute()
