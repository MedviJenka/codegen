from crewai import Crew
from ai.codegen.agents import CustomAgents
from ai.codegen.tasks import AgentTasks
from ai.codegen.tools import ToolKit


tool = ToolKit()
agent = CustomAgents()
tasks = AgentTasks(agent=agent, toolkit=tool)
crew = Crew(agents=[agent.memory_agent()], tasks=[tasks.selenium_task()])
result = crew.kickoff()
print(result)
