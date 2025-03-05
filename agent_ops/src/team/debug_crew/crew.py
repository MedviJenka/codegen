import re
from src.core.executor import Executor
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool, FileReadTool


@CrewBase
class DebugCrew(AzureLLMConfig, Executor):

    """TODO: add rewrite: bool = False"""
    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def debug_agent(self) -> Agent:
        read_tool = FileReadTool(filename=__name__)
        write_tool = FileWriterTool(filename='debugged_code.py')
        return Agent(config=self.agents_config['debug_agent'],
                     verbose=True,
                     llm=self.llm,
                     tools=[read_tool, write_tool])

    @task
    def debug_task(self) -> Task:
        return Task(config=self.tasks_config['debug_task'])

    @crew
    def debug_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def execute(self, error_details: str, original_code: str) -> str:
        """
        Executes AI debugging, analyzes the error, and regenerates fixed code.
        Returns the corrected function as a string.
        """
        print(f"Debugging started with AI Crew...\nError Details: {error_details}")

        # Ensure all required input variables are provided
        inputs = {
            'input': f"Fix this Python function:\n{original_code}\nError:\n{error_details}",
            'function': original_code  # Explicitly passing function code
        }

        # AI Agent Debugging and Code Fixing
        response = self.debug_crew().kickoff(inputs=inputs)

        fixed_code = response.result  # Assuming CrewAI returns corrected code as `result`
        print("AI-generated corrected code:\n", fixed_code)

        # Sanitize AI response: remove markdown artifacts
        fixed_code = re.sub(r"```python\n?|```", "", fixed_code).strip()

        return fixed_code
