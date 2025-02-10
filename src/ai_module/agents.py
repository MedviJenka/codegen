from textwrap import dedent
from crewai import Agent
from src.utils.azure_config import AzureOpenAIConfig
from crewai.telemetry import Telemetry


class WorkaroundHandler:

    @staticmethod
    def _disable_telemetry():

        """Disables telemetry methods temporarily to avoid unwanted behavior."""

        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, lambda *args, **kwargs: None)


class CustomAgents(WorkaroundHandler, AzureOpenAIConfig):

    """Factory class for creating AI agents using CrewAI."""

    def __init__(self) -> None:
        self._disable_telemetry()
        self.llm = self.set_azure_llm

    @property
    def copilot_agent(self) -> Agent:
        return Agent(
            name="Company Copilot",
            role="AI Code Generator",
            instructions="Generate production-ready Python code based on the given prompt.",
            llm=self.llm,
            verbose=True
        )

    def test_plan_agent(self) -> Agent:
        """Creates an agent for generating test plans based on UI analysis."""
        return Agent(
            role="Test Planner",
            goal="Develop structured test plans based on test plan provided.",
            backstory="You are a test planning expert skilled at creating robust test strategies",
            verbose=True,
            llm=self.llm,
        )

    @property
    def page_base_agent(self) -> Agent:
        """Creates an agent for mapping items in a CSV file."""
        return Agent(
            role="CSV Item Mapper",
            goal=dedent("""Identify and categorize items in a CSV file for structured processing.
                        **IMPORTANT**
                        1. change element name by your own logic based on the test plan the the elements your file
                        """),
            backstory=dedent("""
                You specialize in analyzing and mapping CSV file contents into structured formats 
                for efficient data processing and automation.
            """),
            verbose=True,
            llm=self.llm
        )

    def code_agent(self) -> Agent:
        """Creates an agent for generating automation test scripts."""
        return Agent(
            role="Automation Coder",
            goal="Generate test automation scripts based on test plans.",
            backstory=dedent(
                "You are an expert in writing clean, maintainable, and efficient test automation scripts."
            ),
            verbose=True,
            llm=self.llm,
        )

    def security_agent(self) -> Agent:
        """Creates an agent responsible for security analysis of test automation scripts."""
        return Agent(
            role="Security Auditor",
            goal="Identify and mitigate security vulnerabilities in test automation scripts.",
            backstory=dedent(
                """You are an expert security auditor specializing in identifying vulnerabilities 
                in test automation scripts. Your expertise ensures that automation frameworks follow 
                secure coding practices, prevent unauthorized access, and adhere to compliance standards."""
            ),
            verbose=True,
            llm=self.llm,
        )

    def code_review_agent(self) -> Agent:
        """Creates an agent for reviewing test automation scripts."""
        return Agent(
            role="Code Reviewer",
            goal="Ensure test automation scripts follow best practices.",
            backstory=dedent(
                "You are an experienced code reviewer, ensuring test scripts are optimized, "
                "efficient, and follow coding standards."
            ),
            verbose=True,
            llm=self.llm
        )

    def jira_agent(self) -> Agent:
        """Creates an agent for handling Jira ticket automation."""
        return Agent(
            role="Jira Issue Manager",
            goal="Create and manage Jira tickets based on test automation coverage.",
            backstory=dedent(
                "You are an automation specialist who identifies gaps in test automation "
                "coverage and creates Jira tickets to track them."
            ),
            verbose=True,
            llm=self.llm,
        )
