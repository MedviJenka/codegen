from core.logger import Logger
from core.paths import PAGE_BASE
from engine.logic import BrowserRecorder


log = Logger()


def main() -> None:
    try:
        device = input("Enter device type (e.g., 'st', 'mi', or custom): ").strip()
        output_csv = input("Enter output CSV file name (default: 'page_base.csv'): ").strip()
        screen = input("Enter custom screen URL (leave blank to use default for the device): ").strip()
        generate_code = input("Generate code? (y/n): ").strip().lower() == 'y'
        # prompt = input("Add prompt for AI generation (optional):").strip()

        if not output_csv:
            output_csv = PAGE_BASE

        # if not prompt:
        #     pass

        app = BrowserRecorder(device=device, output_csv=output_csv, screen=screen, generate_code=generate_code)
        app.execute()

    except Exception as e:
        log.log_error(f"An error occurred: {e}")
        raise e


if __name__ == '__main__':
    main()
