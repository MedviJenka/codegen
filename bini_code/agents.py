from textwrap import dedent
from crewai import Agent
from bini_ai.engine.azure_config import AzureOpenAIConfig


class CustomAgents:

    def __init__(self) -> None:
        self.config = AzureOpenAIConfig()

    def memory_agent(self):
        return Agent(
            role="Research Specialist",
            goal="Analyze UI elements in an image and generate a test plan.",
            backstory=dedent(
                """As a Research Specialist, your task is to analyze UI elements from a given screenshot, 
                structure them into a JSON format, and generate a comprehensive test plan."""
            ),
            verbose=True,
            llm=self.config.set_azure_llm,
        )
