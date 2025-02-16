from crewai import Flow
from crewai.flow.flow import start, listen
from pydantic import BaseModel
from ai.src.crews.mapping_crew.crew import MappingCrew
from ai.src.crews.test_plan_crew.crew import PlanCrew


class InitialState(BaseModel):
    cache: str = ""


class BiniCode(Flow[InitialState]):

    @start()
    def read_the_test_plan(self) -> None:
        result = PlanCrew().test_plan_crew().kickoff()
        self.state.cache = result.raw
        # with open("test_plan.md", "w") as f:
        #     f.write(result.raw)

    @listen(read_the_test_plan)
    def import_relevant_functions(self) -> None:
        MappingCrew().execute(self.state.cache)


if __name__ == "__main__":
    BiniCode().kickoff()
