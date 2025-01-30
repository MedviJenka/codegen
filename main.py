from logger import Logger
from codegen import BrowserRecorder

log = Logger()

if __name__ == '__main__':
    try:
        # Get inputs interactively from the user
        device = input("Enter device type (e.g., 'st', 'mi', or custom): ").strip()
        output_csv = input("Enter output CSV file name (default: 'page_base.csv'): ").strip()
        screen = input("Enter custom screen URL (leave blank to use default for the device): ").strip()
        generate_code = input("Generate code? (y/n): ").strip().lower() == 'y'
        prompt = input("Add test steps for AI generation").strip()

        # Fallback to default output_csv if the user leaves it blank
        if not output_csv:
            output_csv = "page_base.csv"
        if not prompt:
            prompt = None

        # Initialize the BrowserRecorder with the collected inputs
        app = BrowserRecorder(device=device, output_csv=output_csv, screen=screen if screen else None, generate_code=generate_code)

        # Execute the app
        app.execute()

    except Exception as e:
        log.log_error(f"An error occurred: {e}")
