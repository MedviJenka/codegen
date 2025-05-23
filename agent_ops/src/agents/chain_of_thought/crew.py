from typing import Optional
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from agent_ops.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ChainOfThoughtAgent(AgentInfrastructure):

    def __init__(self, debug: Optional[bool] = False) -> None:
        self.debug = debug
        super().__init__()

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm)

    @task
    def task(self) -> Task:
        return Task(config=self.tasks_config['task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str, original_prompt: str) -> str:
        return self.crew().kickoff({'input': prompt, 'original_prompt': original_prompt}).raw
