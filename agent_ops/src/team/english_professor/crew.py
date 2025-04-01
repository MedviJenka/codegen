from dotenv import load_dotenv
from event_recorder.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


load_dotenv()
FILE = r'C:\Users\evgenyp\PycharmProjects\codegen\agent_ops\src\team\bini\img.png'


@CrewBase
class EnglishProfessor(Executor, AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def grammar_agent(self) -> Agent:
        return Agent(config=self.agents_config['grammar_agent'],
                     verbose=True,
                     llm=self.llm)

    @task
    def grammar_task(self) -> Task:
        return Task(config=self.tasks_config['grammar_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw
