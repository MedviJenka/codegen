from crewai import Crew, Process
from crewai.project import CrewBase, crew
from lab.app.src.app.agents import Agents
from lab.app.src.app.tasks import Tasks
from lab.app.src.app.tools.toolkit import ToolKit
from src.core.paths import TEST_PLAN


@CrewBase
class App(Agents, Tasks):

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.test_agent(),
                    self.function_agent()
            ],
            tasks=[self.test_plan_task(),
                   self.function_mapping_task()
            ],
            process=Process.sequential,
            verbose=True
        )


toolkit = ToolKit()
app = App()
app.crew().kickoff(inputs={'test_plan': toolkit.read_test_plan(path=TEST_PLAN),
                           'get_function': list(toolkit.find_relevant_functions())})
