import logging

from config import settings
from port.client import PortClient
from targets import Slack
from generators import SlackMessageGenerator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Handler:
    @classmethod
    def generate_scorecards_reminders(cls):
        logger.info("Initializing Port client")
        port_client = PortClient(settings.port_api_url, settings.port_client_id, settings.port_client_secret)
        logger.info("Fetching entities")
        entities = port_client.search_entities(
            {
                "combinator": "and",
                "rules": [
                    {
                        "property": "$blueprint",
                        "operator": "=",
                        "value": settings.blueprint
                    },
                    {
                        "property": "$team",
                        "operator": "containsAny",
                        "value": [settings.team]
                    }
                ]
            }
        )
        if settings.target_kind == "slack":
            logger.info(f"Generating scorecards reminders for {len(entities)} entities")
            blocks = SlackMessageGenerator().generate_scorecards_reminders(settings.blueprint,
                                                                           settings.scorecard,
                                                                           entities)
            logger.info("Sending scorecards reminders to slack channel")
            Slack().send_message(blocks)



