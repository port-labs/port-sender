import logging
from typing import Any, Dict, List

from slack_sdk.webhook import WebhookClient

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Slack:
    def __init__(self):
        self.webhook = WebhookClient(settings.slack_webhook_url)

    def send_message(self, blocks: List[Dict[str, Any]]):
        logger.info("Sending message to slack channel")
        response = self.webhook.send(blocks=blocks)

        logger.info("Message sent to slack channel: {response.status_code}")

        return response.status_code
