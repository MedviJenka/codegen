from typing import Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from agent_ops.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ValidationAgent(AgentInfrastructure):

    def __init__(self, debug: Optional[bool] = False) -> None:
        self.debug = debug
        super().__init__()

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.debug)

    @task
    def task(self) -> Task:
        return Task(config=self.tasks_config['task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)

    def execute(self, prompt: str, data: str) -> str:
        result = self.crew().kickoff({'prompt': prompt, 'image_analysis': data})
        return result.raw
