from textwrap import dedent
from crewai import Task, Agent
from dataclasses import dataclass
from bini_code.common import CODE_FORMAT, TASK


@dataclass
class AgentTasks:

    agent: Agent

    def research_screen(self) -> Task:
        return Task(
            description=dedent("Analyze the provided image and identify all UI elements."),
            expected_output=dedent("A JSON report of all identified UI elements."),
            async_execution=False,
            agent=self.agent,
        )

    def create_test_plan(self, ui_elements: str) -> Task:
        return Task(
            description=dedent(
                f"""Based on the detected UI elements, generate a test plan.
                UI Elements:
                {ui_elements}"""
            ),
            expected_output=dedent("A detailed test plan."),
            async_execution=False,
            agent=self.agent,
        )

    def map_elements_task(self) -> None: ...

    def generate_pytest_code(self, device: str, test_plan) -> Task:
        return Task(
            description=dedent(
                f"""Convert the test plan into a functional pytest script but use the code format logic.
                Test Plan: {test_plan}
                Task: {TASK}
                Code Format: {CODE_FORMAT}
                Device: {device}
            """
            ),
            expected_output=dedent("A Python script with pytest tests for the UI elements."),
            async_execution=False,
            agent=self.agent,
        )
