from crewai.crews import CrewOutput
from ai.src.utils.executor import Executor
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from ai.src.tools.toolkit import FunctionMappingTool
from crewai.project import CrewBase, agent, crew, task


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
            tools=[FunctionMappingTool()]
        )

    @task
    def function_task(self) -> Task:
        return Task(config=self.tasks_config['function_task'])

    @task
    def import_module_task(self) -> Task:
        return Task(config=self.tasks_config['import_module_task'])

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
#
#
# m = MappingCrew()
# m.execute("create a call with 2 users")
