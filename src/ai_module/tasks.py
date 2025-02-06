from crewai import Task
from textwrap import dedent
from dataclasses import dataclass
from src.ai_module.tools import ToolKit
from src.ai_module.agents import CustomAgents
from src.utils.common import TASK


@dataclass
class BiniTasks:

    toolkit: ToolKit
    agent = CustomAgents()

    def generate_test(self, test_plan: str, original_code: str) -> Task:
        return Task(
            description=dedent(
                f"""Convert the test plan into a functional pytest script but use the code format logic.
                Test Plan: based on test_plan provided from tool
                Task: {TASK}
                Code Format: {original_code}
                **important**
                1. always log each assertion. example: assert <body> , log.bug('this is a bug') 
                """
            ),
            expected_output=dedent("""A Python script with pytest tests for the UI elements."""),
            async_execution=False,
            agent=self.agent.code_agent(),
            tools=[self.toolkit.read_test_plan_tool(path=test_plan)]
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

    # def python_task(self, file_path: str, content: str) -> Task:
    #     return Task(
    #         description=f'create a clean python code based on this content:\n{content}',
    #         expected_output='python file with clean code',
    #         async_execution=False,
    #         agent=self.agent.code_review_agent(),
    #         tools=[self.toolkit.python_file_tool(file_path=file_path, content=content)])

    def security_check_task(self, updated_code: str) -> Task:
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
            agent=self.agent.jira_agent())
