from dotenv import load_dotenv
from crewai import Crew
from bini_ai.infrastructure.constants import IMAGE_1
from tasks import AgentTasks
from agents import MeetingPreparationAgents

load_dotenv()
tasks = AgentTasks()
agents = MeetingPreparationAgents()


researcher_agent = agents.research_agent()


# Create Tasks
research = tasks.research_screen(image=IMAGE_1, agent=researcher_agent, task='')


# Create Crew responsible for Copy
crew = Crew(
	agents=[researcher_agent],
	tasks=[research]
)


result = crew.kickoff()
print(result)
