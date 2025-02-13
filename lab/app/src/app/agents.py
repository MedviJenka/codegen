import os
import yaml
from crewai import Agent, LLM
from crewai.project import agent, CrewBase
from functools import cached_property


@CrewBase
class Agents:

    """Manages all agent configurations and creation."""

    def __init__(self):
        self.agents = None
        with open("config/agents.yaml", "r", encoding="utf-8") as file:
            self.agents_config = yaml.safe_load(file)

    @cached_property
    def llm(self) -> LLM:
        """Returns the LLM model instance."""
        return LLM(model=os.getenv('MODEL'), api_version=os.getenv('AZURE_API_VERSION'))

    @agent
    def test_agent(self) -> Agent:
        """Creates the test agent."""
        return Agent(
            config=self.agents_config['test_agent'],
            verbose=True,
            llm=self.llm
        )
