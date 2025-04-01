from crewai import Agent, Crew, Process, Task

from agent_ops.src.stories.bini_story import BiniOpsUtils
from agent_ops.src.agents.chain_of_thought.crew import ChainOfThought
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from crewai.project import CrewBase, agent, crew, task


IMAGE = r'C:\Users\evgenyp\PycharmProjects\codegen\agent_ops\src\team\bini\img.png'
SAMPLE_IMAGE = r'C:\Users\evgenyp\PycharmProjects\codegen\agent_ops\src\team\bini\sample_1.png'


class TestBiniOps:

    def test_open_question(self) -> None:
        bini = BiniOpsUtils()
        result = bini.execute(prompt="what name is displayed in this image?", image=IMAGE)
        assert 'Passed' in result

    def test_valid_question(self) -> None:
        bini = BiniOpsUtils()
        result = bini.execute(prompt="what name is displayed in this image?", image=IMAGE)
        assert 'Passed' in result
        assert 'Jenia' in result

    def test_wrong_question(self) -> None:
        bini = BiniOpsUtils()
        result = bini.execute(prompt="what is the name displayed in this picture?", image=IMAGE)
        assert 'Passed' in result
        assert 'Joe' in result

    def test_invalid_question(self) -> None:
        bini = BiniOpsUtils()
        result = bini.execute(prompt="write me a song", image=IMAGE)
        assert 'Invalid Question' in result

    def test_sample_image(self) -> None:
        bini = BiniOpsUtils()
        result = bini.execute(prompt="is the icon displayed in the second image is also displayed in the main?",
                              image=IMAGE,
                              sample_image=SAMPLE_IMAGE)
        assert 'Passed' in result


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


class TestProcess:

    cot = ChainOfThought()

    def test_chain_of_thought(self) -> None:
        result = self.cot.execute("how much is 2 + 2")
        assert '4' in result[0]
