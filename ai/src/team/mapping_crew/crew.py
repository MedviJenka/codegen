from crewai.crews import CrewOutput
from ai.src.tools.toolkit import FunctionMappingForFileReadTool
from ai.src.utils.executor import Executor
from crewai import Agent, Crew, Process, Task
from ai.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from src.core.paths import FUNCTION


@CrewBase
class MappingCrew(AzureLLMConfig, Executor):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def function_agent(self) -> Agent:
        """Agent responsible for processing function-related files."""
        tool = FunctionMappingForFileReadTool(base_dir=FUNCTION)
        python_files = tool.get_all_python_files()

        return Agent(
            config=self.agents_config["function_agent"],
            verbose=True,
            llm=self.llm,
            tools=[FileReadTool(file_path) for file_path in python_files]
        )

    @task
    def function_task(self) -> Task:
        return Task(config=self.tasks_config["function_task"])

    @task
    def import_module_task(self) -> Task:
        return Task(config=self.tasks_config["import_module_task"])

    @task
    def pybrenv_task(self) -> Task:
        return Task(config=self.tasks_config["pybrenv_task"])

    @crew
    def map_crew(self) -> Crew:
        return Crew(
            agents=[self.function_agent()],  # Attach agent dynamically
            tasks=[self.function_task(), self.import_module_task(), self.pybrenv_task()],
            process=Process.sequential,
            verbose=True
        )

    def execute(self, user_input: str) -> CrewOutput:
        """Execute the mapping process on all Python files in a directory."""
        return self.map_crew().kickoff({"query": user_input})


if __name__ == "__main__":
    m = MappingCrew()
    m.execute("")
