from crewai.crews import CrewOutput
from ai.src.utils.executor import Executor
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool


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
            llm=self.llm,
            tools=[FileReadTool(file_path=r'C:\Users\evgenyp\PycharmProjects\codegen\functions\create_call.py')]
        )

    @agent
    def code_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_agent'],
            verbose=True,
            llm=self.llm,
            tools=[FileReadTool(file_path=r'C:\Users\evgenyp\PycharmProjects\codegen\functions\create_call.py')]
        )

    @task
    def function_task(self) -> Task:
        return Task(config=self.tasks_config['function_task'])

    @task
    def import_module_task(self) -> Task:
        return Task(config=self.tasks_config['import_module_task'])

    @task
    def pybrenv_task(self) -> Task:
        return Task(config=self.tasks_config['pybrenv_task'])

    @crew
    def map_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def execute(self, user_input) -> CrewOutput:
        return self.map_crew().kickoff({"query": user_input})
