from crewai import Flow
from crewai.flow.flow import start, listen
from pydantic import BaseModel
from ai.src.crews.mapping_crew.crew import MappingCrew
from ai.src.crews.test_plan_crew.crew import PlanCrew
from src.core.paths import TEST_PLAN


class InitialState(BaseModel):
    cache: str = ""


class BiniCode(Flow[InitialState]):

    @staticmethod
    def read_test_plan(path: str):
        with open(path, "r", encoding="utf-8") as file:
            file.read()

    @start()
    def read_the_test_plan(self) -> None:
        result = PlanCrew().test_plan_crew().kickoff(inputs={'test_plan': self.read_test_plan(TEST_PLAN)})
        self.state.cache = result.raw
        # with open("test_plan.md", "w") as f:
        #     f.write(result.raw)

    @listen(read_the_test_plan)
    def import_relevant_functions(self) -> None:
        MappingCrew().execute(self.state.cache)


BiniCode().kickoff()
