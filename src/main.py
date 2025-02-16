from ai.src.crews.page_base_crew.crew import CSVCrew
from src.core.paths import PAGE_BASE
from src.browser_recorder.workflow import BrowserRecorder


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
        csv_agent = CSVCrew()
        csv_agent.execute()


run_recorder()
