import csv
from src.core.paths import PAGE_BASE
from src.browser_recorder.workflow import BrowserRecorder
from crewai import Flow
from crewai.flow.flow import start, router, listen
from pydantic import BaseModel
from ai.src.team.page_base_crew.crew import CSVCrew


class InitialState(BaseModel):
    cache: list = []
    status: str = ''


class BiniOps(Flow[InitialState]):

    @start()
    def page_base_crew(self) -> None:
        result = CSVCrew().execute()
        self.state.cache.append(result)

    @listen(page_base_crew)
    def validate_csv_content(self) -> None:
        with open(PAGE_BASE, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if not any(row):
                    self.state.status = False
                self.state.status = True

    @router(validate_csv_content)
    def csv_branch(self) -> str:
        if self.state.status:
            return 'success'
        return 'fail'

    @listen('success')
    def success(self) -> None:
        print('CSV file has content')

    @listen('fail')
    def csv_is_empty(self) -> None:
        print('CSV file is empty')


def run_recorder() -> None:
    try:
        device = input("Enter device type (e.g., 'st', 'mi', or custom): ").strip()
        output_csv = input("Enter output CSV file name (default: 'page_base.csv'): ").strip()
        screen = input("Enter custom screen URL (leave blank to use default for the device): ").strip()
        # generate_code = input("Generate code? (y/n): ").strip().lower() == 'n'

        if not output_csv:
            output_csv = PAGE_BASE

        app = BrowserRecorder(device=device, output_csv=output_csv, screen=screen)
        app.execute()

    except Exception as e:
        raise e

    finally:
        BiniOps().kickoff()
        BiniOps().plot()


run_recorder()
