from textwrap import dedent
from typing import Optional
from crewai import Task
from dataclasses import dataclass
from src.ai_module.agents import CustomAgents
from src.ai_module.tools import ToolKit
from src.utils.common import TASK, CODE_FORMAT


@dataclass
class BiniTasks:

    agent: CustomAgents
    toolkit: ToolKit

    def selenium_task(self) -> Task:
        return Task(
            description=dedent("""Analyze the provided image and identify all UI elements."""),
            expected_output=dedent("""A JSON report of all identified UI elements."""),
            async_execution=False,
            agent=self.agent.memory_agent,
            tools=[self.toolkit.selenium_tool(url='https://www.google.com', css_element='.btnK')]
        )

    def research_screen(self) -> Task:
        return Task(
            description=dedent("""Analyze the provided image and identify all UI elements."""),
            expected_output=dedent("""A JSON report of all identified UI elements."""),
            async_execution=False,
            agent=self.agent.memory_agent,

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
            agent=self.agent.test_plan_agent(),  # Fix: Pass an actual Agent instance
        )

    def map_elements_task(self, event_list: list[str]) -> Task:
        return Task(
            description=dedent(f"""
                This list is retrieved from an event listener script, which detects each click on the screen. Use this list to build logic.
                The list contains five elements:
                - element name: Retrieved from element ID, text, or XPath
                - element type: ID, NAME, CSS, XPATH
                - element location: Like XPath or ID 
                - element action: User's action, such as clicking a checkbox, inputting text, etc.
                - value: Exact user input

                Elements List: {event_list}
                """),
            expected_output=dedent("""A Python script with pytest tests for the UI elements."""),
            async_execution=False,
            agent=self.agent.map_elements_agent(),
            # tools=[Tool(name="script_generator", description="Creates automated test scripts based on UI events")]
        )

    def generate_pytest_code(self, test_plan: str, device: Optional[str] = '') -> Task:
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
            agent=self.agent.code_agent(),
            # tools=[Tool(name="pytest_builder", description="Converts test plans into pytest scripts")]
        )

    def code_review_task(self, original_code: str) -> Task:
        return Task(
            description=dedent("""Perform a review of the generated pytest code to ensure quality and correctness."""),
            expected_output=dedent(f"""
                A report with suggested improvements and fixes for the pytest code bellow \n{original_code}.
            """),
            async_execution=False,
            agent=self.agent.code_review_agent(),
            # tools=[Tool(name="code_review", description="Analyzes test scripts for best practices and errors")]
        )

    def security_check(self, updated_code: str) -> Task:
        """Creates a security validation task for automation test scripts."""
        return Task(
            description=dedent(
                f"""
                Perform a security review of the test automation scripts, ensuring 
                they follow best practices and do not contain security vulnerabilities. for this code: \n{updated_code}
                """
            ),
            expected_output=dedent(
                """A report outlining potential security risks in the automation scripts 
                and recommended fixes."""
            ),
            async_execution=False,
            agent=self.agent.code_review_agent()
        )

    def jira_agent_task(self) -> Task:
        return Task(
            description=dedent("""Automatically create Jira tickets for test automation coverage gaps or issues."""),
            expected_output=dedent("""A Jira ticket with relevant details about the missing test cases."""),
            async_execution=False,
            agent=self.agent.jira_agent(),
            # tools=[Tool(name="jira_integration", description="Creates Jira issues for tracking test automation work")]
        )
