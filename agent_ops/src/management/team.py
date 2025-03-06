from event_recorder.core.executor import Executor
from crewai.crews import CrewOutput
from crewai import Agent, Crew, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ManagementTeam(AzureLLMConfig, Executor):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def visionary_strategist(self) -> Agent:
        return Agent(config=self.agents_config['visionary_strategist'],
                     verbose=True,
                     # allow_delegation=True,
                     llm=self.llm)

    @agent
    def logical_analyst(self) -> Agent:
        return Agent(config=self.agents_config['logical_analyst'],
                     verbose=True,
                     # allow_delegation=True,
                     llm=self.llm)

    @agent
    def adaptive_orchestrator(self) -> Agent:
        return Agent(config=self.agents_config['adaptive_orchestrator'],
                     verbose=True,
                     # allow_delegation=True,
                     llm=self.llm)

    @agent
    def compliance_evaluator(self) -> Agent:
        return Agent(config=self.agents_config['compliance_evaluator'],
                     verbose=True,
                     # allow_delegation=True,
                     llm=self.llm)

    @agent
    def execution_commander(self) -> Agent:
        return Agent(config=self.agents_config['execution_commander'],
                     verbose=True,
                     # allow_delegation=True,
                     llm=self.llm)

    @task
    def evaluation_task(self) -> Task:
        return Task(config=self.tasks_config['evaluation_task'])

    @task
    def logical_task(self) -> Task:
        return Task(config=self.tasks_config['logical_task'])

    @task
    def orchestration_task(self) -> Task:
        return Task(config=self.tasks_config['orchestration_task'])

    @task
    def compliance_task(self) -> Task:
        return Task(config=self.tasks_config['compliance_task'])

    @task
    def execution_task(self) -> Task:
        return Task(config=self.tasks_config['execution_task'])

    @crew
    def management(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

    def execute(self, data: str) -> CrewOutput:
        data = {'input': data}
        return self.management().kickoff(inputs=data)


if __name__ == '__main__':
    ManagementTeam().execute('write a poem')
