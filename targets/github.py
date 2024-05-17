import logging
import json
from typing import Any
import time
import requests
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Github:
    def __init__(self) -> None:
        self.api_url = f"{settings.github_api_url}"
        self.auth_value = f"Bearer {settings.github_token}"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": self.auth_value,
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def create_issue(self, issue: dict[str, Any], repository: str) -> dict[str, Any]:
        time.sleep(1)  # To avoid rate limits by github's api
        logger.info(f"Creating new issue at {repository}")
        create_issue_response = requests.request(
            "POST",
            f"{self.api_url}/repos/{repository}/issues",
            json=issue,
            headers=self.headers,
        )

        create_issue_response.raise_for_status()

        return create_issue_response.json()

    def search_issue_by_labels(
        self, labels: list[str], repository: str, state: str = "all"
    ) -> bool:
        logger.info(f"Searching issue with labels {labels}")

        issue_response = requests.request(
            "GET",
            f"{self.api_url}/repos/{repository}/issues",
            headers=self.headers,
            params={"labels": ",".join(labels), "state": state},
        )

        issue_response.raise_for_status()
        return issue_response.json()

    def close_issue(self, issue_number: int, issue: dict[str, Any], repository: str):
        issue["state"] = "closed"
        logger.info(f"Closing issue id {issue_number}")
        return self.update_issue(issue_number, issue, repository)

    def reopen_issue(self, issue_number: int, issue: dict[str, Any], repository: str):
        issue["state"] = "open"
        logger.info(f"Reopening issue id {issue_number}")
        return self.update_issue(issue_number, issue, repository)

    def update_issue(
        self, issue_number: int, updated_issue: dict[str, Any], repository: str
    ):
        logger.info(f"Updating issue id {issue_number}")
        issue_response = requests.request(
            "PATCH",
            f"{self.api_url}/repos/{repository}/issues/{issue_number}",
            headers=self.headers,
            data=json.dumps(updated_issue),
        )
        issue_response.raise_for_status()
        return issue_response.json()
