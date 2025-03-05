from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ChiefExecutiveOfficer(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def chief_executive_officer(self) -> Agent:
        return Agent(config=self.agents_config['chief_executive_officer'],
                     verbose=True,
                     allow_delegation=True,
                     llm=self.llm)

    @task
    def ceo_task(self) -> Task:
        return Task(config=self.tasks_config['ceo_task'])

    @crew
    def ceo(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

    def execute(self, data: str) -> CrewOutput:
        data = {'input': data}
        return self.ceo().kickoff(inputs=data)


chief = ChiefExecutiveOfficer()
chief.execute('write a poem')
