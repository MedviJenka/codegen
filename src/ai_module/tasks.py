from crewai import Task
from textwrap import dedent
from dataclasses import dataclass
from src.ai_module.tools import ToolKit
from src.ai_module.agents import CustomAgents


@dataclass
class BiniTasks:

    toolkit: ToolKit
    agent = CustomAgents()

    def view_test_plan(self, test_plan: str) -> Task:
        return Task(
            description=dedent(f"""Read this test plan {self.toolkit.test_plan_tool(path=test_plan)}"""),
            expected_output=dedent("""A Python script with pytest tests"""),
            async_execution=False,
            agent=self.agent.code_agent())

    def generate_test(self, original_code: str, test_plan: Task) -> Task:
        return Task(
            description=dedent(
                f"""Convert the test plan into a functional pytest script but use the code format logic.
                
                Test Plan: based on test_plan provided from the tool
                
                Task: 
                    based on code format given bellow, if the device is set to smarttap or st: all the imports should be:
                    from qasharedinfra.infra.<smarttap>.general_utils import get_file_size
                    and
                    st: SmartTap = env.devices['Device_1']
                    if the device was set to 'mi' all the imports should include meetinginsights instead of smarttap
                    from qasharedinfra.infra.meetinginsights.selenium.utils.custom_exceptions import ElementIsClickableException
                    and replace st with:
                    mi: MeetingInsightsSaaS = env.devices['Device_1']
                    
                Code Format: {original_code}
                
                **important**
                1. always log each assertion. example: assert <body> , log.bug('this is a bug') 
                2. switch selenium equivalent send_keys() to inject_text()
                3. the amount of tests should be equal to the test plan provided
                4. keep code logic simple and clean
                5. each test must container a docstring 
                """
            ),
            expected_output=dedent("""A Python script with pytest tests"""),
            async_execution=False,
            agent=self.agent.code_agent(),
            depends_on=test_plan,
            # tools=[self.toolkit.read_test_plan_tool(path=test_plan)]
            tools=[self.toolkit.find_functions()]
        )

    def code_review_task(self, original_code: str, generated_code: Task) -> Task:
        return Task(
            description=dedent("""Perform a review of the generated pytest code to ensure quality and correctness."""),
            expected_output=dedent(f"""
                A report with suggested improvements and fixes for the pytest code bellow \n{original_code}.
            """),
            async_execution=False,
            agent=self.agent.code_review_agent(),
            depends_on=generated_code
            # tools=[Tool(name="code_review", description="Analyzes test scripts for best practices and errors")]
        )

    def update_page_base_task(self, event_list: list[str], page_base: str) -> Task:
        return Task(
            description=f"""replace the first items from each list to a logical name {event_list}""",
            expected_output=dedent("""
                                   you will get a list which container lists with 5 elements
                                   input: [[1,2,3,4,5][1,2,3,4,5][1,2,3,4,5]]
                                   input: [[<replace>,2,3,4,5][<replace>,2,3,4,5][<replace>,2,3,4,5]]
                                   """),
            agent=self.agent.page_base_agent,
            function=self.toolkit.update_page_base(data=event_list, page_base=page_base))

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
