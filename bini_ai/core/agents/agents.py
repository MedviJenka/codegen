from crewai import Agent
from textwrap import dedent
from dataclasses import dataclass
from bini_ai.engine.azure_config import AzureOpenAIConfig


@dataclass
class CustomAgent:

    """
    Notes for agents:
        1. Agents should be result driven and have a clear goal in mind
        2. Role is their job title
        3. Goal should be actionable
        4. Backstory should be their resume

    """

    config: AzureOpenAIConfig

    @property
    def prompt_expert_agent(self) -> Agent:
        return (Agent(
            role='Prompt Expert',
            goal=dedent("Rephrasing user prompt in a more professional way"),
            backstory=dedent("""Rephrasing user prompt in more professional way"""),
            allow_delegation=False,
            llm=self.config.set_azure_llm,
            verbose=True))

    @property
    def element_memory_agent(self) -> Agent:

        """
          Returns an Agent instance configured as a Prompt Expert.

          This agent's primary role is to rephrase user prompts in a more professional manner.
          The goal and backstory of the agent are both centered around refining user inputs
          to ensure they are presented in a polished and professional way. This agent does
          not allow delegation of tasks and operates with verbosity enabled.

          Returns:
              Agent: An instance of the Agent class configured for prompt rephrasing.

        """

        return Agent(
            role='Element Page Mapping Expert',
            goal=dedent(f"""map each element as logical as you can based on given screenshots and memory them"""),
            backstory=dedent(f"""Professional screenshot expert"""),
            allow_delegation=True,
            llm=self.config.set_azure_llm,
            verbose=True)

    @property
    def test_plan_agent(self) -> Agent:

        """
          Returns an Agent instance configured as a Prompt Expert.

          This agent's primary role is to rephrase user prompts in a more professional manner.
          The goal and backstory of the agent are both centered around refining user inputs
          to ensure they are presented in a polished and professional way. This agent does
          not allow delegation of tasks and operates with verbosity enabled.

          Returns:
              Agent: An instance of the Agent class configured for prompt rephrasing.

        """

        return Agent(
            role='QA Automation Agent Expert',
            goal=dedent(f"""creating test plans based on given description"""),
            backstory=dedent(f"""Professional screenshot expert"""),
            allow_delegation=True,
            llm=self.config.set_azure_llm,
            verbose=True)

    @property
    def code_expert_agent(self) -> Agent:

        """
          Returns an Agent instance configured as a Prompt Expert.

          This agent's primary role is to rephrase user prompts in a more professional manner.
          The goal and backstory of the agent are both centered around refining user inputs
          to ensure they are presented in a polished and professional way. This agent does
          not allow delegation of tasks and operates with verbosity enabled.

          Returns:
              Agent: An instance of the Agent class configured for prompt rephrasing.

        """

        return Agent(
            role='Code Expert',
            goal=dedent(f"""creating a pytest code based on code given"""),
            backstory=dedent(f"""Professional automation engineer with qa and security expertise"""),
            allow_delegation=True,
            llm=self.config.set_azure_llm,
            verbose=True)
