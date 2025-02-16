from src.core.paths import PAGE_BASE
from src.browser_recorder.workflow import BrowserRecorder
from crewai import Flow
from crewai.flow.flow import start, listen
from pydantic import BaseModel
from ai.src.crews.page_base_crew.crew import CSVCrew
from ai.src.crews.py_crew.crew import PyCrew
from time import sleep


class InitialState(BaseModel):
    cache: list = []


class BiniOps(Flow[InitialState]):

    @start()
    def page_base_crew(self) -> None:
        result = CSVCrew().execute()
        self.state.cache.append(result)

    @listen(page_base_crew)
    def code_crew(self) -> None:
        result = PyCrew().execute()
        self.state.cache.append(result)


def run_recorder() -> None:
    try:
        device = input("Enter device type (e.g., 'st', 'mi', or custom): ").strip()
        output_csv = input("Enter output CSV file name (default: 'page_base_beofre_ai.csv'): ").strip()
        screen = input("Enter custom screen URL (leave blank to use default for the device): ").strip()
        generate_code = input("Generate code? (y/n): ").strip().lower() == 'y'

        if not output_csv:
            output_csv = PAGE_BASE

        app = BrowserRecorder(device=device, output_csv=output_csv, screen=screen, generate_code=generate_code)
        app.execute()

    except Exception as e:
        raise e

    finally:
        # wait fo csv and python templates to be generated
        sleep(10)
        BiniOps().kickoff()


run_recorder()
