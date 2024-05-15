import base64
import logging
from typing import Any

import requests

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Github:
    def __init__(self) -> None:
        self.api_url = f"{settings.github_api_url}"

        auth_message = f"{settings.github_email}:{settings.github_token}"
        auth_bytes = auth_message.encode("ascii")
        b64_bytes = base64.b64encode(auth_bytes)
        b64_message = b64_bytes.decode("ascii")
        self.auth_value = f"Basic {b64_message}"
        self.headers = {
            "Accept": "application/vnd.github.raw+json",
            "Content-Type": "application/vnd.github.raw+json",
            "Authorization": self.auth_value,
        }

    def create_issue(self, params: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"Creating new issue: {params['fields']['summary']}")

        create_issue_response = requests.request(
            "POST", f"{self.api_url}/issues", json=params, headers=self.headers
        )

        create_issue_response.raise_for_status()

        return create_issue_response.json()

    def search_issue_by_labels(self, labels: list[str], owner: str, repo: str) -> bool:
        logger.info(f"Searching issue with labels {labels}")
        issue_response = requests.request(
            "GET",
            f"{self.api_url}/repos/{owner}/{repo}/issues",
            headers=self.headers,
            params={"label": ",".join(labels)},
        )

        issue_response.raise_for_status()
        return issue_response.json()

    def resolve_issue(self, issue: dict[str, Any], owner: str, repo: str):
        issue["state"] = "closed"
        logger.info(f"Resolving issue id {issue['id']}")
        return self.update_issue(issue, owner, repo)

    def reopen_issue(self, issue: dict[str, Any], owner: str, repo: str):
        issue["state"] = "closed"
        logger.info(f"Reopening issue id {issue['id']}")
        return self.update_issue(issue, owner, repo)

    def update_issue(self, updated_issue: dict[str, Any], owner: str, repo: str):
        logger.info(f"Updating issue id {updated_issue['id']}")
        issue_response = requests.request(
            "PATCH",
            f"{self.api_url}/repos/{owner}/{repo}/issues/{updated_issue['id']}",
            headers=self.headers,
            body=updated_issue,
        )

        issue_response.raise_for_status()
        return issue_response.json()
