import base64
import logging
from typing import Any
from urllib.parse import quote

import requests
from requests.auth import HTTPBasicAuth

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Jira:
    def __init__(self) -> None:
        self.auth = HTTPBasicAuth(settings.jira_email, settings.jira_token)
        self.api_url = f"{settings.jira_api_endpoint}/rest/api/3"

        auth_message = f"{settings.jira_email}:{settings.jira_token}"
        auth_bytes = auth_message.encode("ascii")
        b64_bytes = base64.b64encode(auth_bytes)
        b64_message = b64_bytes.decode("ascii")
        self.auth_value = f"Basic {b64_message}"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.auth_value,
        }

    def create_issue(self, params: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"Creating new issue: {params['fields']['summary']}")

        create_issue_response = requests.request(
            "POST", f"{self.api_url}/issue", json=params, headers=self.headers
        )

        create_issue_response.raise_for_status()

        return create_issue_response.json()

    def search_issue(self, jql_query: str) -> bool:

        issue_response = requests.request(
            "GET",
            f"{self.api_url}/search?jql={quote(jql_query, safe='')}",
            headers=self.headers,
        )

        issue_response.raise_for_status()
        return issue_response.json()

    def resolve_issue(self, issue: dict[str, Any]):
        issue_fields = issue["fields"]
        key = issue["key"]
        logger.info(f"Resolving {issue_fields['issuetype']['name']}:"
                    f" {key} - "
                    f"{issue_fields['summary']}")

        if not settings.jira_resolve_transition_id:
            # Looking for a default resolve transition id
            logger.info("Jira transition id parameter was not inserted,"
                        " getting the default from the Jira project")

            transitions_response = requests.request(
                "GET",
                f"{self.api_url}/issue/{key}/transitions",
                headers=self.headers
            ).json()
            resolved_transition = next((t["id"] for t in transitions_response["transitions"]
                                        if t['to']['name'] == 'Done'), None)
        else:
            resolved_transition = settings.jira_resolve_transition_id

            if not resolved_transition:
                logger.info("Jira transition to done was not found,"
                            " please enter the jira_resolve_transition_id parameter")
                return

        return self.transition_issue(key, resolved_transition)

    def reopen_issue(self, issue: dict[str, Any]):
        issue_fields = issue["fields"]
        key = issue["key"]
        logger.info(f"Reopening {issue_fields['issuetype']['name']}:"
                    f" {key} - "
                    f"{issue_fields['summary']}")

        if not settings.jira_reopen_transition_id:

            transitions_response = requests.request(
                "GET",
                f"{self.api_url}/issue/{key}/transitions",
                headers=self.headers
            ).json()
            reopen_transition = next((t["id"] for t in transitions_response["transitions"]
                                      if t['to']['name'] == 'To Do'), None)
        else:
            reopen_transition = settings.jira_reopen_transition_id

            if not reopen_transition:
                logger.info("Jira transition to To Do was not found,"
                            " please enter the jira_resolve_transition_id parameter")
                return

        return self.transition_issue(key, reopen_transition)

    def transition_issue(self, issue_key: str, transition_id: str):
        body = {"transition": {"id": transition_id}}
        issue_response = requests.request(
            "POST",
            f"{self.api_url}/issue/{issue_key}/transitions",
            headers=self.headers,
            json=body,
        )

        issue_response.raise_for_status()
        return issue_response
