import logging

from config import settings
from generators.slack import SlackMessageGenerator
from targets.slack import Slack

from core.base_handler import BaseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SlackHandler(BaseHandler):
    def scorecard_reminder(self):
        if not self.entities:
            logger.info("No entities found")
            return

        logger.info(
            f"Generating scorecards reminders for {len(self.entities)} entities"
        )
        blocks = SlackMessageGenerator().scorecard_reminder(
            settings.blueprint, self.scorecard, self.entities
        )
        logger.info("Sending scorecards reminders to slack channel")
        Slack().send_message(blocks)

    def scorecard_report(self):
        if not self.entities:
            logger.info("No entities found")
            return

        logger.info(f"Generating scorecard report for {len(self.entities)} entities")
        blocks = SlackMessageGenerator().scorecard_report(
            settings.blueprint, self.scorecard, self.entities
        )
        logger.info("Sending scorecard report to slack channel")
        Slack().send_message(blocks)
