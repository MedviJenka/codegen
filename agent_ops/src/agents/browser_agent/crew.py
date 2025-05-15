from dotenv import load_dotenv
from crewai_tools import BrowserbaseLoadTool
from crewai import Agent, Crew, Task
from event_recorder.core.executor import Executor
from crewai.project import CrewBase, agent, crew, task
from agent_ops.src.utils.azure_llm import AzureLLMConfig
from agent_ops.src.agents.browser_agent.tools import SearchTools


load_dotenv()


browserbase_tool = BrowserbaseLoadTool()

# Extract the text from the site
text = browserbase_tool.run("https://www.google.com")
print(text)


@CrewBase
class BrowserAgent(AzureLLMConfig, Executor):

    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'],
                     verbose=True, llm=self.llm,
                     tools=[SearchTools.search_internet, browserbase_tool])

    @task
    def task(self) -> Task:
        return Task(config=self.tasks_config['task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)

    def execute(self, prompt: str) -> str or list:
        result = self.crew().kickoff({'prompt': prompt})
        return result.raw


if __name__ == '__main__':
    agent = BrowserAgent()
    agent.execute(prompt='search for cats')
