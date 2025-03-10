import os
import csv
import urllib3
from time import sleep
from typing import Optional
from playwright.sync_api import sync_playwright
from event_recorder.engine.credentials import USERNAME, PASSWORD
from event_recorder.core.executor import Executor
from event_recorder.core.logger import Logger
from event_recorder.core.paths import PAGE_BASE, PYTHON_CODE, JS_SCRIPT


urllib3.disable_warnings()
log = Logger()


class BrowserRecorder(Executor):

    """
    TODO:
        1. Find element by id, name. if using xpath find by value .............. WIP
        2. Compare original page base with temp one.
           * first with value
           * second with name using AI
        3. Replace relevant rows

    """

    def __init__(self,
                 device: str,
                 output_csv: str = PAGE_BASE,
                 screen: Optional[str] = None,
                 generate_code: Optional[bool] = False,
                 prompt: Optional[str] = '') -> None:

        self.device = device
        self.generate_code = generate_code
        self.prompt = prompt
        self.interactions = []
        self.recorded_elements = set()
        self.output_csv = output_csv

        # Check if a custom screen is provided, and override defaults if so
        if screen:
            self.screen = screen
        elif self.device == 'st':
            self.screen = 'https://irqa.ai-logix.net'
        elif self.device == 'mi':
            self.screen = 'https://misquad01.ai-logix.net'
        elif self.device is None:
            pass
        else:
            raise ValueError("A valid screen URL must be provided for custom devices.")

    @property
    def __read_script(self) -> str:
        with open(JS_SCRIPT, 'r', encoding='utf-8') as file:
            return file.read()

    def __compare_page_base_elements(self, original: str, temp: str) -> None:
        """compares generated csv to original one"""


    def run(self) -> None:
        """Run the browser and automate interactions."""
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Inject JavaScript to capture interactions
                page.add_init_script(self.__read_script)
                page.goto(self.screen)
                sleep(2)

                log.log_info("Login meeting insights")
                page.click("#signIn")
                page.fill(selector="#i0116", value=USERNAME)
                page.click("#idSIButton9")
                page.fill(selector="#i0118", value=PASSWORD)
                page.click("#idSIButton9")
                page.click("#idSIButton9")

                log.log_info("Interact with the browser if needed. Close it when you're done.")

                while True:
                    try:
                        # Evaluate only if the page is still open
                        if not page.is_closed():
                            new_interactions = page.evaluate("""
                                (() => {
                                    let unique = [];
                                    let seen = new Set();
                                    for (let i of window.recordedInteractions) {
                                        let key = JSON.stringify(i);
                                        if (!seen.has(key)) {
                                            seen.add(key);
                                            unique.push(i);
                                        }
                                    }
                                    window.recordedInteractions = []; // Clear after fetching
                                    return unique;
                                })()
                            """)

                            if new_interactions:
                                for interaction in new_interactions:
                                    element_identifier = (
                                        interaction["tag_name"],
                                        interaction["id"] or interaction["name"] or interaction["xpath"],
                                    )
                                    if element_identifier not in self.recorded_elements:
                                        tag_name = interaction["tag_name"]
                                        element_type = (
                                            "id" if interaction["id"]
                                            else "name" if interaction["name"]
                                            else "xpath"
                                        )
                                        element_path = interaction["id"] or interaction["name"] or interaction["xpath"]
                                        action_description = interaction["action_description"]
                                        value = interaction.get("value")

                                        self.interactions.append(
                                            [tag_name, element_type.upper(), element_path, action_description, value])
                                        self.recorded_elements.add(element_identifier)

                                # Clear interactions
                                page.evaluate("window.recordedInteractions = []")
                            else:
                                # Avoid tight infinite loop
                                page.wait_for_timeout(300)

                    except Exception as e:
                        log.log_info(f"Navigation or context issue: {e}")
                        if "closed" in str(e):
                            break
            except Exception as e:
                log.log_info(f"Error during execution: {e}")

            finally:
                try:
                    browser.close()
                except Exception as e:
                    log.log_info(f"Error closing the browser: {e}")

    def save_to_csv(self) -> None:

        """Save the unique interactions to a CSV file."""
        if not os.path.isdir(self.output_csv):
            os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Element Name", "Element Type", "Element Path", "Action", "Value"])
            writer.writerows(self.get_interactions())  # Use unique interactions

    def get_interactions(self) -> list:
        """Return unique recorded interactions (no duplicates)."""
        seen = set()
        unique_interactions = []

        for interaction in self.interactions:
            key = (interaction[0], interaction[1], interaction[2], interaction[3], interaction[4])  # Unique identifier
            if key not in seen and interaction[4] != "None":  # Ensure we don't log 'None' values
                seen.add(key)
                unique_interactions.append(interaction)

        return unique_interactions

    @property
    def events_to_dict(self):
        keys = ["element_ame", "element_type", "element_path", "action", "value"]
        return [dict(zip(keys, values)) for values in self.get_interactions()]

    def __generate_methods(self, function_name: str) -> str:

        code_cache = []

        for each_list in self.get_interactions():

            tag_name = each_list[0]
            action = each_list[3]
            value = each_list[4]

            # Fix Click Actions
            if "Clicked" in action:
                code_cache.append(f"    device.get_mapped_element('{tag_name}').action(Actions.CLICK)")

            # Fix Typing Actions - Only add inject_text if there's an actual value
            if "Typed" in action or "typing" in action:
                if value and value.strip():  # Avoid 'None' or empty values
                    code_cache.append(f"    device.get_mapped_element('{tag_name}').inject_text('{value}')")

            # Handle checkbox interactions correctly
            if action.startswith("Checkbox checked"):
                code_cache.append(f"    device.get_mapped_element('{tag_name}').action(Actions.CLICK)")

        # Ensure proper indentation for the final generated code
        methods_code = "\n".join(code_cache)  # Preserve indentation

        final_code = f"""def test_{function_name}(device) -> None:\n{methods_code}"""

        log.log_info(final_code)
        return final_code

    @staticmethod
    def __create_python_file(output: str) -> None:
        with open(PYTHON_CODE, "w") as file:
            file.write(output)
        log.log_info(f'python file: {PYTHON_CODE}')

    def execute(self, **kwargs: any) -> None:

        """Execute the browser recorder."""

        try:
            self.run()
            self.save_to_csv()
            self.get_interactions()
            log.log_info("\nRecorded Interactions:")
            log.log_info(f'{self.get_interactions()}')
            log.log_info(f"\nInteractions saved to {self.output_csv}")

            code = self.__generate_methods(function_name=kwargs.get('function_name'))
            self.__create_python_file(output=code)

        except Exception as e:
            log.log_error(f'error: {e}')
