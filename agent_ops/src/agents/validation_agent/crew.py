from crewai.crews import CrewOutput
from dotenv import load_dotenv
from event_recorder.core.executor import Executor
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


load_dotenv()


@CrewBase
class ValidationAgent(Executor, AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def validation_agent(self) -> Agent:
        return Agent(config=self.agents_config['validation_agent'], verbose=True, llm=self.llm)

    @task
    def validation_task(self) -> Task:
        return Task(config=self.tasks_config['validation_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)

    def execute(self, data: str) -> str:
        result = self.crew().kickoff({'data': data})
        return result.raw
