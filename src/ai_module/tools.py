import csv
import requests
from typing import Optional
from crewai_tools import SeleniumScrapingTool, FileReadTool
from src.core.dir_mapping import FunctionDiscovery


class ToolKit(FunctionDiscovery):

    @staticmethod
    def selenium_tool(url: str, css_element: Optional[str] = None) -> SeleniumScrapingTool:
        return SeleniumScrapingTool(
            website_url=url,
            css_element=css_element  # '.main-content'
        )

    def find_functions(self) -> any:
        return self.functions_index.items()

    @staticmethod
    def copilot(api_key: str) -> requests:
        """for now copilot unable to generate code"""
        url = f"https://api.github.com/enterprises/audiocodes-emu/copilot/metrics"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.github+json",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.text}"

    @staticmethod
    def update_page_base(data: list[str], page_base: str) -> None:
        with open(page_base, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['Element Name', 'Element Type', 'Element Path', 'Action', 'Value'])
            writer.writerows(data)

    @staticmethod
    def read_test_plan_tool(path: str) -> FileReadTool:
        return FileReadTool(file_path=path)

    # @staticmethod
    # def __create_python_file(file_path: str, content: str) -> str:
    #     """Saves the generated Python code to a .py file."""
    #     try:
    #         with open(file_path, "w", encoding="utf-8") as file:
    #             file.write(content)
    #         return f"Python file saved successfully at {file_path}"
    #     except Exception as e:
    #         return f"Error saving Python file: {e}"
    #
    # def python_file_tool(self, file_path: str, content: str):
    #     return Tool(name="SavePythonFile",
    #                 description="Saves Python code to a .py file.",
    #                 function=self.__create_python_file(file_path=file_path, content=content))


t = ToolKit()
for each in t.find_functions():
    print(each)
