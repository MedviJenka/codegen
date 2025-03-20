from typing import Optional
from dotenv import load_dotenv
from agent_ops.src.team.bini.image_handler import CompressAndUploadImage
from event_recorder.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


load_dotenv()


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
                     llm=self.llm)

    @task
    def vision_task(self) -> Task:
        return Task(config=self.tasks_config['vision_task'])

    @task
    def compare_task(self) -> Task:
        return Task(config=self.tasks_config['compare_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self, prompt: str, image_path: str, sample_image: Optional[str or list] = '') -> CrewOutput:
        compressor = CompressAndUploadImage()
        image = compressor.upload_image(image_path=image_path)
        return self.crew().kickoff({'prompt': prompt, 'image': image, 'sample_image': sample_image})

