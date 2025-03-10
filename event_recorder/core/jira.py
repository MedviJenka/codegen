import os
import urllib3
from atlassian import Jira
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass
from event_recorder.core.logger import Logger


logger = Logger()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class JiraFactory:

    url: str = "https://acjira"
    cloud: bool = True
    verify_ssl: bool = False

    @property
    def get_token(self) -> str:
        load_dotenv()
        return os.getenv('JIRA_TOKEN')

    def __post_init__(self):
        """Initialize Jira API connection."""
        try:
            self.jira = Jira(url=self.url, token=self.get_token, cloud=self.cloud, verify_ssl=self.verify_ssl)
            logger.log_info("Connected to Jira successfully.")
        except Exception as _e:
            logger.log_error(f"Failed to connect to Jira: {_e}")
            raise


@dataclass
class JiraTicket:

    jira_factory: JiraFactory
    project_name: str
    summary: str
    issue_type: str
    description: Optional[str] = "",

    def create_ticket(self) -> dict:

        """Creates a new Jira issue and returns the response."""

        payload = {
            "project": {"key": self.project_name},
            "summary": self.summary,
            "description": self.description,
            "issuetype": {"name": self.issue_type},
        }

        try:
            response = self.jira_factory.jira.issue_create(fields=payload)
            logger.log_info(f"Jira ticket created successfully: {response}")
            return response
        except Exception as e:
            logger.log_error(f"Failed to create Jira ticket: {e}")
            raise


if __name__ == "__main__":
    try:
        jira_factory = JiraFactory()
        ticket = JiraTicket(
            jira_factory=jira_factory,
            project_name="STNG",
            summary="Automated Jira ticket",
            issue_type="Bug",
            description="This is a test issue created using the Jira REST API.")

        ticket_response = ticket.create_ticket()
        logger.log_info(f"Created ticket response: {ticket_response}")
    except Exception as e:
        logger.log_error(f"Error: {e}")
