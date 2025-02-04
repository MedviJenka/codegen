from crewai import Task
from textwrap import dedent


class AgentTasks:

	@staticmethod
	def research_screen(agent):
		return Task(
			description=dedent(f"""Analyze the provided image and identify all UI elements."""),
			expected_output=dedent(f"""
				A JSON-formatted report containing a breakdown of each identified UI element,  
				including its logical name, type, and intended use case.
			"""),
			async_execution=True,
			agent=agent,
		)
