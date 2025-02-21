from crewai import Agent, Crew, Process, Task
from crewai.crews import CrewOutput
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.vision_tool.vision_tool import VisionTool

from ai.src.tools.toolkit import ImageVisionTool
from ai.src.utils.azure_llm import AzureLLMConfig
VisionTool()


# from ai.src.crews.new_bini.bini.src.bini.tools.custom_tool import ImageCompressionTool


@CrewBase
class BiniCrew(AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    # If you would like to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def english_agent(self) -> Agent:
        return Agent(config=self.agents_config["english_agent"], llm=self.llm)

    @agent
    def image_agent(self) -> Agent:
        return Agent(config=self.agents_config["image_agent"], llm=self.llm)

    @task
    def english_task(self) -> Task:
        return Task(config=self.tasks_config["english_task"])

    @task
    def image_task(self) -> Task:
        return Task(config=self.tasks_config["image_task"], tools=[ImageVisionTool()])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents,
                    tasks=self.tasks,
                    process=Process.sequential,
                    verbose=True)

    def execute(self, prompt: str, image_path: str) -> CrewOutput:
        return self.crew().kickoff(inputs={'prompt': prompt, 'image': image_path})


bini = BiniCrew()
bini.execute(prompt='what do you seen in this image?', image_path=r'C:\Users\evgenyp\PycharmProjects\codegen\ai\src\crews\new_bini\bini\src\bini\tools\image.png')
