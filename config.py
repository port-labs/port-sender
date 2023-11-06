from enum import Enum

from pydantic_settings import BaseSettings


class MessageKind(str, Enum):
    generate_scorecards_reminders = "generate_scorecards_reminders"


class TargetKind(str, Enum):
    slack = "slack"


class Settings(BaseSettings):
    port_api_url: str = "https://api.getport.io"
    port_client_id: str
    port_client_secret: str
    slack_webhook_url: str
    team: str
    blueprint: str
    scorecard: str
    message_kind: MessageKind = MessageKind.generate_scorecards_reminders
    target_kind: TargetKind = TargetKind.slack

    class Config:
        env_prefix = "INPUT_"


settings = Settings()
