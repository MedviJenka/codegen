from src.core.paths import PAGE_BASE
from src.browser_recorder.workflow import BrowserRecorder
from src.infrastructure.utils import BiniCodeUtils
from dataclasses import dataclass


@dataclass
class BiniBrowserRecorder:

    bini: BiniCodeUtils

    def run_bini_recorder(self) -> None:
        try:
            device = input("Enter device type (e.g., 'st', 'mi', or custom): ").strip()
            output_csv = input("Enter output CSV file name (default: 'page_base.csv'): ").strip()
            screen = input("Enter custom screen URL (leave blank to use default for the device): ").strip()
            generate_code = input("Generate code? (y/n): ").strip().lower() == 'y'

            if not output_csv:
                output_csv = PAGE_BASE

            app = BrowserRecorder(device=device, output_csv=output_csv, screen=screen, generate_code=generate_code)
            app.execute(self.bini)

        except Exception as e:
            raise e


if __name__ == '__main__':
    utils = BiniCodeUtils()
    bini = BiniBrowserRecorder(bini=utils)
    bini.run_bini_recorder()
