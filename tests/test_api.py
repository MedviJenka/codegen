from crewai.crews import CrewOutput
from crewai import Agent, Crew, Process, Task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class SanityAgent(AzureLLMConfig):

    agents: list[Agent] = None
    tasks: list[Agent] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'],
                     verbose=True,
                     llm=self.llm)

    @task
    def task(self) -> Task:
        return Task(config=self.tasks_config['task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


class TestSanity:

    agent = SanityAgent()

    def test_execute(self) -> None:
        result = self.agent.crew().kickoff().raw
        assert result == 'Hello'
