from typing import Optional
from dotenv import load_dotenv
from src.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai_tools import VisionTool
from crewai.project import CrewBase, agent, crew, task


load_dotenv()
FILE = r'./img.png'


@CrewBase
class Bini(Executor, AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def vision_agent(self) -> Agent:
        return Agent(config=self.agents_config['vision_agent'],
                     verbose=True,
                     llm=self.llm,
                     tools=[VisionTool(image_url_path=FILE)])

    @task
    def vision_task(self) -> Task:
        return Task(config=self.tasks_config['vision_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self, inputs: str, raw_output: Optional[str] = False) -> CrewOutput or str:
        match raw_output:
            case True:
                return self.crew().kickoff({'image': inputs}).raw
            case _:
                return self.crew().kickoff({'image': inputs})


m = Bini()
m.execute(inputs='whats the name?')
