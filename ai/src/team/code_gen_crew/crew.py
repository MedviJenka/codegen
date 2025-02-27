from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.file_writer_tool.file_writer_tool import FileWriterTool
from src.core.paths import PYTHON_CODE, OUTPUT_PATH


@CrewBase
class CodegenCrew(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def code_agent(self) -> Agent:
        return Agent(config=self.agents_config['code_agent'],
                     verbose=True,
                     tools=[
                         FileReadTool(file_path=PYTHON_CODE),
                         FileWriterTool(directory=OUTPUT_PATH, overwrite=True)],
                     llm=self.llm)

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config['code_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self) -> CrewOutput:
        return self.crew().kickoff()
