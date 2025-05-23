import csv
from time import sleep
from src.core.paths import PAGE_BASE
from src.browser_recorder.workflow import BrowserRecorder
from crewai import Flow
from crewai.flow.flow import start, router, listen
from pydantic import BaseModel
from agent_ops.src.agents.page_base_agent.crew import PageBaseCrew


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
            next(reader)
            for row in reader:
                if any(row):
                    self.state.status = True

    @router(validate_csv_content)
    def csv_branch(self) -> str:
        if self.state.status:
            return 'router_success'
        return 'router_fail'

    # @listen('router_success')
    # def generate_code(self) -> None:
    #     print('CSV file has content, running PyCrew which generates PyBREnv code')
    #     CodegenCrew().execute()
    #
    # @listen('router_fail')
    # def csv_is_empty(self) -> None:
    #     print('CSV file is empty, please check the file and try again')


def main() -> None:
    device = 'mi'
    browser = BrowserRecorder(device=device)
    try:
        browser.execute()
        # sleep(10)
    finally:
        ...
        # PageBaseFlow().kickoff()


if __name__ == '__main__':
    main()
