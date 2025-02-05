import csv
import urllib3
from typing import Optional
from dotenv import load_dotenv
from event_listener import init_code, JS_SCRIPT
from playwright.sync_api import sync_playwright
from src.core.executor import Executor
from src.core.logger import Logger
from src.core.paths import PAGE_BASE, PYTHON_CODE
from src.infrastructure.utils import BiniCodeUtils


urllib3.disable_warnings()
load_dotenv()
log = Logger()


class BrowserRecorder(Executor):

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
            self.screen = 'https://devngming.ai-logix.net'
        else:
            raise ValueError("A valid screen URL must be provided for custom devices.")

    def run(self) -> None:
        """Run the browser and automate interactions."""
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Inject JavaScript to capture interactions
                page.add_init_script(JS_SCRIPT)
                page.goto(self.screen)

                log.log_info("Interact with the browser if needed. Close it when you're done.")

                while True:
                    try:
                        # Evaluate only if the page is still open
                        if not page.is_closed():
                            new_interactions = page.evaluate("window.recordedInteractions || []")
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
        """Save the interactions to a CSV file."""
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Element Name", "Element Type", "Element Path", "Action", "Value"])
            writer.writerows(self.interactions)

    def get_interactions(self) -> list:
        """Return the list of recorded interactions."""
        return self.interactions

    def __generate_methods(self, scenario: str, test_name: str) -> str:

        code_cache = []

        for each_list in self.get_interactions():
            tag_name = each_list[0]
            action = each_list[3]
            value = each_list[4]

            if action == 'Clicked on button':
                code_cache.append(f"driver.get_mapped_element('{tag_name}').action(Actions.CLICK)")
            elif action == 'Clicked on input' and value is not None:
                code_cache.append(f"driver.get_mapped_element('{tag_name}').inject_text('{value}')")
            elif action == 'Typed in input':
                code_cache.append(f"driver.get_mapped_element('{tag_name}').inject_text('{value}')")
            elif action.startswith('Clicked on'):
                code_cache.append(f"driver.get_mapped_element('{tag_name}').action(Actions.CLICK)")
            elif action.startswith('Checkbox checked'):
                code_cache.append(f"driver.get_mapped_element('{tag_name}').action(Actions.CLICK)")

        methods_code = "\n".join(code_cache)  # Ensure proper indentation for generated code

        # Ensure overall indentation for the final generated code
        final_code = f"""
        {init_code(device=self.device)}
        class Test{scenario}:

            def test_{test_name}(self, driver) -> None:
                {methods_code}
        """
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

            log.log_info("\nRecorded Interactions:")
            log.log_info(f'{self.get_interactions()}')
            log.log_info(f"\nInteractions saved to {self.output_csv}")
            bini = BiniCodeUtils()
            bini.execute(event_list=self.interactions)
            # code = self.__generate_methods(scenario=kwargs.get('scenario'), test_name=kwargs.get('test_name'))

            # if self.generate_code:
            #     self.__create_python_file(output=code)

        except Exception as e:
            log.log_error(f'error: {e}')
