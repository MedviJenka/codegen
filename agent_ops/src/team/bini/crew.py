import base64
from dotenv import load_dotenv
from event_recorder.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
from typing import Optional, Type
from crewai.tools import BaseTool
from openai import OpenAI
from pydantic import BaseModel, validator, field_validator


load_dotenv()
FILE = r'./img.png'


class ImagePromptSchema(BaseModel):
    image_path: str = "The image path or URL."


class VisionTool(BaseTool):

    name: str = "Vision Tool"
    description: str = "This tool uses OpenAI's Vision API to describe the contents of an image."
    args_schema: Type[BaseModel] = ImagePromptSchema

    def _run(self, **kwargs) -> str:
        try:
            image_path_url = kwargs.get("image_path_url")
            if not image_path_url:
                return "Image Path or URL is required."

            # Validate input using Pydantic
            ImagePromptSchema(image_path_url=image_path_url)

            if image_path_url.startswith("http"):
                image_data = image_path_url
            else:
                try:
                    base64_image = self._encode_image(image_path_url)
                    image_data = f"data:image/jpeg;base64,{base64_image}"
                except Exception as e:
                    return f"Error processing image: {str(e)}"

            response = self.langchain_llm.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_data},
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"An error occurred: {str(e)}"

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


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

    def execute(self, prompt: str, raw_output: Optional[str] = False) -> CrewOutput or str:
        match raw_output:
            case True:
                return self.crew().kickoff({'prompt': prompt}).raw
            case _:
                return self.crew().kickoff({'prompt': prompt})


m = Bini()
m.execute(prompt='whats the name?')
