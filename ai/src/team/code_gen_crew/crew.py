from ai.src.tools.tools import ToolKit
from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.file_writer_tool.file_writer_tool import FileWriterTool


@CrewBase
class CodegenCrew(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def code_agent(self) -> Agent:
        file_tool = FileWriterTool(file_name='app.py')

        return Agent(config=self.agents_config['code_agent'],
                     verbose=True,
                     tools=[file_tool],
                     llm=self.llm)

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config['code_task'])

    @crew
    def map_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self, functions: any) -> list[CrewOutput]:
        tool = ToolKit()
        data = [{'tool': str(tool.index_functions)}]
        return self.map_crew().kickoff_for_each(inputs=data)


CodegenCrew().execute(functions=None)
