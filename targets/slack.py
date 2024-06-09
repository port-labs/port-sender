import logging
from typing import Any, Dict, List

from slack_sdk.webhook import WebhookClient

from config import settings

logger = logging.getLogger(__name__)


class Slack:
    def __init__(self):
        self.webhook = WebhookClient(settings.slack_webhook_url)

    def send_message(self, blocks: List[Dict[str, Any]]):
        logger.info("Sending message to slack channel")
        response = self.webhook.send(blocks=blocks)
        if response.status_code > 200:
            raise Exception(f"Failed to send Message to slack channel: {response.status_code}, {response.body}, "
                            f"slack channel: {settings.slack_webhook_url}, blocks: {blocks}")
        logger.info(f"Message sent to slack channel: {response.status_code}, {response.body}")
        return response.status_code
