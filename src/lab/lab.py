import csv
from crewai import Agent, Task, Crew
from src.utils.azure_config import AzureOpenAIConfig


# Define a function to write to CSV
def write_to_csv(data, filename=r"C:\Users\evgenyp\PycharmProjects\codegen\src\output\page_base.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Age", "Role"])  # Header
        writer.writerows(data)


# Define an Agent
agent = Agent(name="Data Writer",
              role="CSV Manager",
              goal="Write structured data into a CSV file.",
              backstory="An AI assistant that manages CSV records efficiently.",
              llm=AzureOpenAIConfig().set_azure_llm)

# Define a Task
task = Task(
    description="Write user data into a CSV file.",
    agent=agent,
    expected_output="CSV file should contain user details.",
    function=write_to_csv([["Alice", 30, "Engineer"], ["Bob", 25, "Designer"]])
)

# Create and run the Crew
crew = Crew(agents=[agent], tasks=[task])
crew.kickoff()
