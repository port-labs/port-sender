import logging
import json
from typing import Any, Optional
import time
import requests
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REQUESTS_BACKOFF_FACTOR = 60


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
        time.sleep(1)  # https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28#pause-between-mutative-requests
        logger.info(f"Creating new issue at {repository}")
        create_issue_response = self._send_request(
            "POST",
            f"{self.api_url}/repos/{repository}/issues",
            data=json.dumps(issue),
            headers=self.headers,
        )

        create_issue_response.raise_for_status()

        return create_issue_response.json()

    def search_issue_by_labels(
        self, labels: list[str], repository: str, state: str = "all"
    ) -> bool:
        logger.info(f"Searching issue with labels {labels}")

        issue_response = self._send_request(
            "GET",
            f"{self.api_url}/repos/{repository}/issues",
            headers=self.headers,
            params={"labels": ",".join(labels), "state": state},
        )
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
        time.sleep(1)  # https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28#pause-between-mutative-requests
        logger.info(f"Updating issue id {issue_number}")
        issue_response = self._send_request(
            "PATCH",
            f"{self.api_url}/repos/{repository}/issues/{issue_number}",
            headers=self.headers,
            data=json.dumps(updated_issue),
        )
        return issue_response.json()

    def _send_request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, str]] = None,
        data: Optional[str] = None,
    ):
        max_retries = 3
        backoff_factor = REQUESTS_BACKOFF_FACTOR
        status_forcelist = [403, 429]

        for attempt in range(max_retries):
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
            )
            if response.status_code not in status_forcelist:
                response.raise_for_status()
                return response
            else:
                sleep_time = backoff_factor * (2**attempt)
                logger.warning(f"Got rate-limited, sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
