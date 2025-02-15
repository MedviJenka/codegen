from crewai import Flow
from crewai.flow.flow import start, listen
from pydantic import BaseModel
from ai.src.crews.test_plan_crew.crew import PlanCrew
from ai.src.tools.custom_tool import FunctionMapping
from src.core.paths import TEST_PLAN


class InitialState(BaseModel):
    cache: str = ""


class BiniCode(Flow[InitialState]):

    @start()
    def read_the_test_plan(self) -> None:
        read_test_plan = lambda path: open(path, "r", encoding="utf-8").read()
        result = PlanCrew().test_plan_crew().kickoff(inputs={'test_plan': read_test_plan(TEST_PLAN)})
        self.state.cache = result.raw
        with open("test_plan.md", "w") as f:
            f.write(result.raw)

    @listen(read_the_test_plan)
    def import_relevant_functions(self) -> None:
        mapping = FunctionMapping()
        print(mapping.execute_function(self.state.cache))

    # @listen(get_asterisk)
    # def import_relevant_functions(self) -> None:
    #     relevant_functions = MappingCrew().execute(self.state.cache)
    #     self.state.cache = relevant_functions
    #


BiniCode().kickoff()
