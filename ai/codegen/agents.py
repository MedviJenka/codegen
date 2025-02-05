from textwrap import dedent
from crewai import Agent
from ai.codegen.azure_config import AzureOpenAIConfig
from functools import cached_property


class CustomAgents:
    """Factory class for creating AI agents using CrewAI."""

    @cached_property
    def config(self) -> AzureOpenAIConfig:
        """Lazily initializes and returns Azure OpenAI config."""
        return AzureOpenAIConfig()

    def selenium_agent(self) -> Agent:
        """Creates an agent for Selenium-based web scraping."""
        return Agent(
            role="Selenium Scraper",
            goal="Extract element attributes from web pages.",
            backstory=dedent("You are an expert web scraper specializing in Selenium automation."),
            verbose=True,
            llm=self.config.set_azure_llm,
        )

    def memory_agent(self) -> Agent:
        """Creates an agent for analyzing UI elements and generating a test plan."""
        return Agent(
            role="Research Specialist",
            goal="Analyze UI elements from images and generate structured test plans.",
            backstory=dedent(
                "As a Research Specialist, your task is to analyze UI elements from screenshots, "
                "structure them into JSON format, and generate a comprehensive test plan."
            ),
            verbose=True,
            llm=self.config.set_azure_llm,
        )

    def test_plan_agent(self) -> Agent:
        """Creates an agent for generating test plans based on UI analysis."""
        return Agent(
            role="Test Planner",
            goal="Develop structured test plans based on UI elements.",
            backstory=dedent(
                "You are a test planning expert skilled at creating robust test strategies "
                "from UI elements detected in images."
            ),
            verbose=True,
            llm=self.config.set_azure_llm,
        )

    def map_elements_agent(self) -> Agent:
        """Creates an agent for mapping UI elements into testable components."""
        return Agent(
            role="UI Element Mapper",
            goal="Identify and categorize UI elements for automated testing.",
            backstory=dedent(
                "You specialize in mapping UI elements into structured formats "
                "for automation test creation."
            ),
            verbose=True,
            llm=self.config.set_azure_llm,
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
            llm=self.config.set_azure_llm,
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
            llm=self.config.set_azure_llm,
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
            llm=self.config.set_azure_llm,
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
            llm=self.config.set_azure_llm,
        )
