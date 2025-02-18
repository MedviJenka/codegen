import traceback
import inspect
from functools import wraps
from src.core.executor import Executor
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class DebugCrew(AzureLLMConfig, Executor):
    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def debug_agent(self) -> Agent:
        return Agent(config=self.agents_config['debug_agent'],
                     verbose=True,
                     llm=self.llm)

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
        return fixed_code


def ai():
    """Decorator that wraps test functions, invokes DebugCrew on failure, and auto-corrects code."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_trace = traceback.format_exc()
                print(f"Test failed in {func.__name__}. Triggering DebugCrew...\n{error_trace}")

                # Extract source code of the function
                original_code = inspect.getsource(func)

                # Debug and Fix Code via AI Agent
                debug_team = DebugCrew()
                fixed_code = debug_team.execute(error_trace, original_code)

                # Execute the corrected function dynamically
                exec_globals = {}
                exec(fixed_code, globals(), exec_globals)

                # Re-run the fixed function
                if func.__name__ in exec_globals:
                    print(f"Re-running the corrected function: {func.__name__}")
                    exec_globals[func.__name__]()
                else:
                    print("Error: AI failed to generate a valid function.")

        return wrapper

    return decorator


@ai()
def test_app():
    assert 1 + 1 == 3  # This will trigger AI debugging


# Run the test function
test_app()
