from src.core.executor import Executor
from crewai import Agent, Crew, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class VisionaryStrategist(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def visionary_strategist(self) -> Agent:
        return Agent(config=self.agents_config['visionary_strategist'],
                     verbose=True,
                     allow_delegation=True,
                     llm=self.llm)

    @task
    def evaluation_task(self) -> Task:
        return Task(config=self.tasks_config['evaluation_task'])

    @crew
    def management(self) -> Crew:
        return Crew(
            agents=[self.visionary_strategist()],
            tasks=[self.evaluation_task()],
            verbose=True,
        )

    def execute(self, data: str) -> None:
        self.management().kickoff(inputs={'input': data})


v = VisionaryStrategist()
v.execute('write a poem')
