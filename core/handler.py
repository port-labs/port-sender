import logging

from config import settings, TargetKind
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
        logger.info(
            f"Fetching entities for query: {settings.filter_rule}, blueprint {settings.blueprint}, scorecard {settings.scorecard}")
        search_query = {
            "combinator": "and",
            "rules": [
                {
                    "property": "$blueprint",
                    "operator": "=",
                    "value": settings.blueprint
                }
            ],
        }
        if settings.filter_rule:
            search_query["rules"].append(settings.filter_rule.dict())

        entities = port_client.search_entities(
            search_query
        )
        scorecard = port_client.get_scorecard(settings.blueprint, settings.scorecard).get("scorecard")
        if not entities:
            logger.info("No entities found")
            return
        if settings.target_kind == TargetKind.slack:
            logger.info(f"Generating scorecards reminders for {len(entities)} entities")
            blocks = SlackMessageGenerator().generate_scorecards_reminders(settings.blueprint,
                                                                           scorecard,
                                                                           entities)
            logger.info("Sending scorecards reminders to slack channel")
            Slack().send_message(blocks)

    @classmethod
    def generate_scorecard_report(cls):
        logger.info("Initializing Port client")
        port_client = PortClient(settings.port_api_url, settings.port_client_id, settings.port_client_secret)
        logger.info(
            f"Fetching entities for query: {settings.filter_rule}, blueprint {settings.blueprint}, scorecard {settings.scorecard}")
        search_query = {
            "combinator": "and",
            "rules": [
                {
                    "property": "$blueprint",
                    "operator": "=",
                    "value": settings.blueprint
                }
            ],
        }
        if settings.filter_rule:
            search_query["rules"].append(settings.filter_rule.dict())

        entities = port_client.search_entities(
            search_query
        )
        scorecard = port_client.get_scorecard(settings.blueprint, settings.scorecard).get("scorecard")
        if not entities:
            logger.info("No entities found")
            return
        if settings.target_kind == TargetKind.slack:
            logger.info(f"Generating scorecard report for {len(entities)} entities")
            blocks = SlackMessageGenerator().generate_scorecard_report(settings.blueprint,
                                                                       scorecard,
                                                                       entities)
            logger.info("Sending scorecard report to slack channel")
            Slack().send_message(blocks)




