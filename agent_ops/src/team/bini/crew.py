import base64
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from event_recorder.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig, CompressAndUploadToOpenAI
from crewai.project import CrewBase, agent, crew, task
from typing import Optional, Type
from crewai.tools import BaseTool
from crewai_tools import VisionTool
from pydantic import BaseModel


load_dotenv()
FILE = r'C:\Users\evgenyp\PycharmProjects\codegen\agent_ops\src\team\bini\img.png'


class ImagePromptSchema(BaseModel):

    prompt: str = 'user prompt'
    image_path: str = "The image path or URL."


class CustomVisionTool(BaseTool):

    name: str = "Vision Tool"
    description: str = "This tool uses OpenAI's Vision API to describe the contents of an image."
    args_schema: Type[BaseModel] = ImagePromptSchema

    @staticmethod
    def __compress(image_path: str):
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image

    def __upload_image(self, image_path: str, prompt: str = "Describe this image"):
        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.__compress(image_path)}"}}
        ])

        response = self.langchain_llm.invoke([message])

        print(response.content)
        return response

    def _run(self, image_path: str, prompt: str) -> str:

        if not image_path:
            return "Image Path or URL is required."

        return self.__upload_image(image_path=image_path, prompt=prompt)


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
                     llm=self.langchain_llm,
                     tools=[CustomVisionTool()])

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

    def execute(self, prompt: str, image_path: str) -> CrewOutput or str:
        return self.crew().kickoff({'prompt': prompt, 'image_path': image_path})


m = Bini()
m.execute(prompt='whats the name?', image_path=FILE)
