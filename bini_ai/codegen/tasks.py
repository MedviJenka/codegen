from textwrap import dedent
from typing import Optional
from crewai import Task, Agent
from dataclasses import dataclass
from bini_ai.codegen.common import TASK, CODE_FORMAT


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

    def map_elements_task(self, event_list: list[str]) -> Task:
        return Task(
            description=dedent(
                f"""This list is retrieved from event listener script, which detects each click on my screen, use this list to build a logic.
                the list contains five elements [
                    element name: which is retrieved from element id text or xapth
                    element type: ID, NAME, CSS, XPATH
                    element location: like xpath or id 
                    element action: users action such as click on checkbox, input text in field etc 
                    value: exact users input
                ]
                Elements List: {event_list}
            """
            ),
            expected_output=dedent("A Python script with pytest tests for the UI elements."),
            async_execution=False,
            agent=self.agent,
        )

    def generate_pytest_code(self, test_plan, device: Optional[str] = '') -> Task:
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
