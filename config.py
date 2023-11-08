from enum import Enum
from typing import List, Union, Optional

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings


class MessageKind(str, Enum):
    scorecard_reminder = "scorecard_reminder"
    scorecard_report = "scorecard_report"


class TargetKind(str, Enum):
    slack = "slack"


class FilterRule(BaseModel):
    property: str
    operator: str
    value: Union[str, int, List[str], List[int]] = None


class Settings(BaseSettings):
    port_client_id: str
    port_client_secret: str
    slack_webhook_url: str
    port_region: str = "eu"
    blueprint: str
    scorecard: str
    filter_rule: Union[FilterRule, str, None] = Field(default=None)
    message_kind: MessageKind = MessageKind.scorecard_reminder
    target_kind: TargetKind = TargetKind.slack

    class Config:
        env_prefix = "INPUT_"


settings = Settings()
