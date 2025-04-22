from typing import Optional
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from agent_ops.src.agent_ops.src.agents.computer_vision.image import CompressAndUploadImage
from agent_ops.src.agent_ops.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ComputerVisionAgent(AgentInfrastructure):

    def __init__(self, debug: Optional[bool] = False) -> None:
        self.debug = debug
        super().__init__(debug=self.debug)

    @agent
    def vision_agent(self) -> Agent:
        return Agent(config=self.agents_config['vision_agent'], llm=self.llm, verbose=self.debug)

    @task
    def vision_task(self) -> Task:
        return Task(config=self.tasks_config['vision_task'])

    @task
    def decision_task(self) -> Task:
        return Task(config=self.tasks_config['decision_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str, image_path: str, sample_image: Optional[list or str] = '') -> str:
        compressor = CompressAndUploadImage()
        image = compressor.upload_image(prompt='', image_path=image_path, sample_image=sample_image)
        return self.crew().kickoff({'prompt': prompt, 'image': image, 'sample_image': sample_image}).raw
