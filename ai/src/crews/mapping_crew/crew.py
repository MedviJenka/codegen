from crewai import Agent, Crew, Process, Task
from crewai.crews import CrewOutput
from crewai.project import CrewBase, agent, crew, task
from ai.src.utils.azure_llm import AzureLLMConfig
from ai.src.utils.executor import Executor


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

    @agent
    def code_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_agent'],
            verbose=True,
            llm=self.llm
        )

    @task
    def function_task(self) -> Task:
        return Task(config=self.tasks_config['function_task'])

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

    def execute(self, user_input, function_index, **kwargs) -> CrewOutput:

        return self.map_crew().kickoff({"query": user_input,
                                        "available_functions": function_index,
                                        'response': kwargs})

