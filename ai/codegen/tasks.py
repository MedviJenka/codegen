from textwrap import dedent
from typing import Optional
from crewai import Task
from ai.codegen.agents import CustomAgents
from ai.codegen.common import TASK, CODE_FORMAT
from ai.codegen.tools import ToolKit


class AgentTasks:

    """TODO: test what suits better, custom agent or built-in agent"""

    def __init__(self, agent: CustomAgents, toolkit: ToolKit):
        self.agent = agent
        self.toolkit = toolkit

    def selenium_task(self) -> Task:
        return Task(
            description=dedent("""Analyze the provided image and identify all UI elements."""),
            expected_output=dedent("""A JSON report of all identified UI elements."""),
            async_execution=False,
            agent=self.agent.memory_agent(),
            tools=[self.toolkit.selenium_tool(url='https://www.google.com', css_element='.btnK')]
        )

    def research_screen(self) -> Task:
        return Task(
            description=dedent("""Analyze the provided image and identify all UI elements."""),
            expected_output=dedent("""A JSON report of all identified UI elements."""),
            async_execution=False,
            agent=self.agent.memory_agent(),

        )

    def create_test_plan(self, ui_elements: str) -> Task:
        return Task(
            description=dedent(
                f"""Based on the detected UI elements, generate a test plan.
                UI Elements:
                {ui_elements}"""
            ),
            expected_output=dedent("""A detailed test plan."""),
            async_execution=False,
            agent=self.agent,
            # tools=[Tool(name="test_generation", description="Generates a structured test plan from UI elements")]
        )

    def map_elements_task(self, event_list: list[str]) -> Task:
        return Task(
            description=dedent(
                f"""This list is retrieved from an event listener script, which detects each click on the screen. Use this list to build logic.
                The list contains five elements:
                - element name: Retrieved from element ID, text, or XPath
                - element type: ID, NAME, CSS, XPATH
                - element location: Like XPath or ID 
                - element action: User's action, such as clicking a checkbox, inputting text, etc.
                - value: Exact user input

                Elements List: {event_list}
                """
            ),
            expected_output=dedent("""A Python script with pytest tests for the UI elements."""),
            async_execution=False,
            agent=self.agent,
            # tools=[Tool(name="script_generator", description="Creates automated test scripts based on UI events")]
        )

    def generate_pytest_code(self, test_plan, device: Optional[str] = '') -> Task:
        return Task(
            description=dedent(
                f"""Convert the test plan into a functional pytest script but use the code format logic.
                Test Plan: {test_plan}
                Task: {TASK}
                Code Format: {CODE_FORMAT}
                Device: {device}"""
            ),
            expected_output=dedent("""A Python script with pytest tests for the UI elements."""),
            async_execution=False,
            agent=self.agent,
            # tools=[Tool(name="pytest_builder", description="Converts test plans into pytest scripts")]
        )

    def code_review_task(self) -> Task:
        return Task(
            description=dedent("""Perform a review of the generated pytest code to ensure quality and correctness."""),
            expected_output=dedent("""A report with suggested improvements and fixes for the pytest code."""),
            async_execution=False,
            agent=self.agent,
            # tools=[Tool(name="code_review", description="Analyzes test scripts for best practices and errors")]
        )

    def jira_agent_task(self) -> Task:
        return Task(
            description=dedent("""Automatically create Jira tickets for test automation coverage gaps or issues."""),
            expected_output=dedent("""A Jira ticket with relevant details about the missing test cases."""),
            async_execution=False,
            agent=self.agent,
            # tools=[Tool(name="jira_integration", description="Creates Jira issues for tracking test automation work")]
        )
