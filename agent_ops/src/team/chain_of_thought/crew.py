from dotenv import load_dotenv
from event_recorder.core.executor import Executor
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from typing import Generic, TypeVar


load_dotenv()
COT = TypeVar('COT', bound='ChainOfThought')


class IChainOfThought(Generic[COT], AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"


@CrewBase
class ChainOfThought(IChainOfThought, Executor):

    @agent
    def chain_of_thought_agent(self) -> Agent:
        return Agent(config=self.agents_config['chain_of_thought_agent'], verbose=True, llm=self.llm)

    @task
    def chain_of_thought_task(self) -> Task:
        return Task(config=self.tasks_config['chain_of_thought_task'])

    @crew
    def crew(self) -> Crew:
        return Crew( agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)

    def execute(self, prompt: str) -> list:
        result = self.crew().kickoff({'prompt': prompt}).raw
        thought_list = result.split('*')
        return thought_list
