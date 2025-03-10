from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from agent_ops.src.tools.toolkit import ReadTestPlanTool
from agent_ops.src.utils.azure_llm import AzureLLMConfig


@CrewBase
class PlanCrew(AzureLLMConfig):

    agents = None
    tasks = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def test_plan_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['test_plan_agent'],
            verbose=True,
            llm=self.llm,
            tools=[ReadTestPlanTool()]
        )

    @task
    def test_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_plan_task'],
        )

    @crew
    def test_plan_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def execute(self) -> None:
        self.test_plan_crew().kickoff(inputs={'review': 'review this test plan'})


PlanCrew().execute()
