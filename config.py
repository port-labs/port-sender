from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class OperationKind(str, Enum):
    scorecard_reminder = "scorecard_reminder"
    scorecard_report = "scorecard_report"
    ticket_creator = "ticket_handler"
    issue_handler = "issue_handler"


class TargetKind(str, Enum):
    slack = "slack"
    jira = "jira"
    github = "github"


class FilterRule(BaseModel):
    property: str
    operator: str
    value: Union[str, int, List[str], List[int]] = None


class Settings(BaseSettings):
    port_client_id: str
    port_client_secret: str
    github_api_url: str = ""
    github_token: str = ""
    github_repository: str = ""
    slack_webhook_url: str = ""
    jira_project_id: str = ""
    jira_api_endpoint: str = "https://jira.com"
    jira_email: str = ""
    jira_resolve_transition_id: str = ""
    jira_reopen_transition_id: str = ""
    jira_token: str = ""
    port_region: str = "eu"
    blueprint: str
    scorecard: str
    filter_rule: Union[FilterRule, str, None] = Field(default=None)
    operation_kind: OperationKind = OperationKind.scorecard_reminder
    target_kind: TargetKind = TargetKind.slack
    log_level: str = "INFO"

    class Config:
        env_prefix = "INPUT_"


settings = Settings()
