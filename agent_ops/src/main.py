import random
from crewai import Flow
from pydantic import BaseModel
from crewai.flow.flow import start, listen, and_, router
from agent_ops.src.CEO.ceo import ChiefExecutiveOfficer
from agent_ops.src.management.team import ManagementTeam
# from ai.src.team.mapping_crew.crew import MappingCrew
from agent_ops.src.agents.page_base_agent.crew import CSVCrew
# from ai.src.team.py_crew.crew import PyCrew
# from ai.src.team.test_plan_crew.crew import PlanCrew


class InitialState(BaseModel):
    cache: str = ""
    number: int = random.randint(a=1, b=2)


class BiniOps(Flow[InitialState]):

    def csv_team(self) -> None:
        result = CSVCrew().execute()
        self.state.cache = result

    # @start()
    # def management(self) -> None:
    #     management_team = ManagementTeam().execute(data='write a poem')
    #     self.state.cache = management_team.raw
    #
    # @listen(and_(management))
    # def ceo(self) -> None:
    #     ceo = ChiefExecutiveOfficer().execute(data=self.state.cache)
    #     self.state.cache = ceo

    @router
    def __element_branch(self) -> str:

        if self.state.number == 1:
            return 'success'
        else:
            return 'fail'

    # @start()
    # def page_base_crew(self) -> None:
    #     result = CSVCrew().execute()
    #     self.state.cache = result
    #
    # @listen(page_base_crew)
    # def code_crew(self) -> None:
    #     result = PyCrew().execute()
    #     self.state.cache = result

    # @start()
    # def read_the_test_plan(self) -> None:
    #     result = PlanCrew().test_plan_crew().kickoff()
    #     self.state.cache = result.raw
    #
    # @listen(read_the_test_plan)
    # def import_relevant_functions(self) -> None:
    #     MappingCrew().execute(self.state.cache)


ops = BiniOps()
ops.kickoff()
ops.plot()

