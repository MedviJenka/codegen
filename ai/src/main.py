from crewai import Flow
from crewai.flow.flow import start, listen
from pydantic import BaseModel
from ai.src.crews.mapping_crew.crew import MappingCrew
from ai.src.crews.page_base_crew.crew import CSVCrew
from ai.src.crews.py_crew.crew import PyCrew
from ai.src.crews.test_plan_crew.crew import PlanCrew


class InitialState(BaseModel):
    cache: str = ""


class BiniOps(Flow[InitialState]):

    @start()
    def page_base_crew(self) -> None:
        result = CSVCrew().execute()
        self.state.cache = result

    @listen(page_base_crew)
    def py_crew(self) -> None:
        result = PyCrew().execute()
        self.state.cache = result
        
    # @start()
    # def read_the_test_plan(self) -> None:
    #     result = PlanCrew().test_plan_crew().kickoff()
    #     self.state.cache = result.raw
    #
    # @listen(read_the_test_plan)
    # def import_relevant_functions(self) -> None:
    #     MappingCrew().execute(self.state.cache)

