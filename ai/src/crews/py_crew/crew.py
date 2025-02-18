from crewai.crews import CrewOutput
from src.core.executor import Executor
from src.core.paths import PYTHON_CODE, AI_PYTHON_CODE
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai_tools import FileWriterTool, FileReadTool
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class PyCrew(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def code_agent(self) -> Agent:
        return Agent(config=self.agents_config['code_agent'],
                     verbose=True,
                     llm=self.llm,
                     tools=[
                         FileReadTool(file_path=PYTHON_CODE),
                         FileWriterTool(filename=AI_PYTHON_CODE, overwrite=True)])

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config['code_task'])

    @crew
    def code_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self) -> CrewOutput:
        return self.code_crew().kickoff()
