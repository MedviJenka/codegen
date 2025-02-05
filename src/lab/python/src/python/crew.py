from functools import cached_property

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.utils.azure_config import AzureOpenAIConfig


# Uncomment the following line to use an example of a custom tool
# from python.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@CrewBase
class PythonCrew:
	"""Python crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@cached_property
	def config(self) -> AzureOpenAIConfig:
		"""Lazily initializes and returns Azure OpenAI config."""
		return AzureOpenAIConfig()

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=self.config.set_azure_llm
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Python crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=2)
