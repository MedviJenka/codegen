from typing import Optional
from crewai_tools import SeleniumScrapingTool


class ToolKit:

    @staticmethod
    def selenium_tool(url: str, css_element: Optional[str] = None) -> SeleniumScrapingTool:
        return SeleniumScrapingTool(
            website_url=url,
            css_element=css_element  # '.main-content'
        )
