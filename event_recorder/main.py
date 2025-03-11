import csv
from time import sleep
from event_recorder.core.paths import PAGE_BASE
from event_recorder.engine.workflow import BrowserRecorder
from crewai import Flow
from crewai.flow.flow import start, router, listen
from pydantic import BaseModel
from agent_ops.src.team.page_base_crew.crew import PageBaseCrew


device = 'mi'


class InitialState(BaseModel):

    cache: list = []
    status: bool = False


class PageBaseFlow(Flow[InitialState]):

    """
    TODO
        1. concentrate on specific screen like action items
        2. prove that this tool can handle clicks and inject test
        ---
        phase 2:

    """

    @start()
    def page_base_crew(self) -> None:
        result = PageBaseCrew().execute()
        self.state.cache.append(result)

    @listen(page_base_crew)
    def validate_csv_content(self) -> None:
        with open(PAGE_BASE, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # first row
            try:
                next(reader)  # skip to second row
                self.state.status = True
            except StopIteration:
                self.state.status = False
                pass

    @router(validate_csv_content)
    def csv_branch(self) -> str:
        if self.state.status:
            return 'router_success'
        return 'router_fail'

    @listen('router_success')
    def generate_code_based_on_new_csv(self) -> None:
        print('CSV file has content, running code generation')

    @listen('router_fail')
    def csv_is_empty(self) -> None:
        print('CSV file is empty, please check the file and try again')


def run_event_listener() -> None:
    browser = BrowserRecorder(device=device)
    browser.execute(function_name='meeting_insights')


if __name__ == '__main__':
    run_event_listener()
    # PageBaseFlow().kickoff()
