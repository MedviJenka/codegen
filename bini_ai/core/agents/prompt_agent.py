from bini_ai.infrastructure.enums import Prompts
from bini_ai.core.agents.manager import AgentManager


class SetAgent(AgentManager):

    """
    Enhances and validates prompts and results using agents and crews.
    """

    def enhance_prompt(self, prompt: str) -> str:
        """
        Enhances a given prompt using the prompt agent and a supporting agent.

        :param prompt: The prompt to enhance.
        :return: The enhanced prompt result.
        """
        crew = self.create_task_crew(
            task_description="Rephrase prompt in a more professional text {input}",
            task_output="professional prompt engineer: {input}",
            agent=self.prompt_agent,
            supporting_role="prompt expert",
            supporting_goal="Rephrase {input}",
            supporting_backstory="Professional Rephrase Agent"
        )

        return self.process_with_crew(crew, prompt)

    def set_memory_agent(self, result) -> str:

        """
        Validates a given result using the validation agent and a supporting agent.

        :param result: The result to validate.
        :return: The validated result.
        """

        crew = self.create_task_crew(
            task_description="{input}",
            task_output="{input}",
            agent=self.element_memory_agent,
            supporting_role=Prompts.element_memory_prompt,
            supporting_goal="validate {input} in a professional manner",
            supporting_backstory="You're a professional prompt validation engineer"
        )

        return self.process_with_crew(crew, result)

    # def set_test_plan_agent(self, result: str) -> str:
    #
    #     """
    #     Validates a given result using the validation agent and a supporting agent.
    #
    #     :param result: The result to validate.
    #     :return: The validated result.
    #     """
    #
    #     crew = self.create_task_crew(
    #         task_description="{input}",
    #         task_output="{input}",
    #         agent=self.validation_agent,
    #         supporting_role=Prompts.validation_agent,
    #         supporting_goal="validate {input} in a professional manner",
    #         supporting_backstory="You're a professional prompt validation engineer"
    #     )
    #
    #     return self.process_with_crew(crew, result)
    #
    # def set_code_expert_agent(self, result: str) -> str:
    #
    #     """
    #     Validates a given result using the validation agent and a supporting agent.
    #
    #     :param result: The result to validate.
    #     :return: The validated result.
    #     """
    #
    #     crew = self.create_task_crew(
    #         task_description="{input}",
    #         task_output="{input}",
    #         agent=self.validation_agent,
    #         supporting_role=Prompts.validation_agent,
    #         supporting_goal="validate {input} in a professional manner",
    #         supporting_backstory="You're a professional prompt validation engineer"
    #     )
    #
    #     return self.process_with_crew(crew, result)
