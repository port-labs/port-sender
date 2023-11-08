from enum import Enum
from typing import List, Union, Optional

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings


class MessageKind(str, Enum):
    generate_scorecards_reminders = "generate_scorecards_reminders"
    generate_scorecard_report = "generate_scorecard_report"


class TargetKind(str, Enum):
    slack = "slack"


class FilterRule(BaseModel):
    property: str
    operator: str
    value: Union[str, int, List[str], List[int]] = None


class Settings(BaseSettings):
    port_api_url: str = "https://api.getport.io"
    port_client_id: str
    port_client_secret: str
    slack_webhook_url: str
    blueprint: str
    scorecard: str
    filter_rule: Optional[FilterRule] = Field(default=None)
    message_kind: MessageKind = MessageKind.generate_scorecards_reminders
    target_kind: TargetKind = TargetKind.slack

    class Config:
        env_prefix = "INPUT_"


settings = Settings()
