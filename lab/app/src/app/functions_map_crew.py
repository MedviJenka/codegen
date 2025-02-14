import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from lab.app.src.app.config.azure_llm import AzureLLMConfig


@CrewBase
class FunctionMapCrew(AzureLLMConfig):

    def __init__(self):
        self.agents = None
        self.tasks = None

        with open("config/agents.yaml", "r", encoding="utf-8") as file:
            self.agents_config = yaml.safe_load(file)
        with open("config/tasks.yaml", "r", encoding="utf-8") as file:
            self.tasks_config = yaml.safe_load(file)

    @agent
    def function_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['function_mapping_agent'],
            verbose=True,
            llm=self.llm
        )

    @task
    def function_task(self) -> Task:
        return Task(
            config=self.tasks_config['function_mapping_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
