import logging

from config import settings
from port.client import PortClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseHandler:
    def __init__(self):
        logger.info("Initializing Port client")
        port_client = PortClient(
            settings.port_region, settings.port_client_id, settings.port_client_secret
        )
        logger.info(
            f"Fetching entities for query:"
            f" {settings.filter_rule},"
            f" blueprint {settings.blueprint},"
            f" scorecard {settings.scorecard}"
        )
        search_query = {
            "combinator": "and",
            "rules": [
                {"property": "$blueprint", "operator": "=", "value": settings.blueprint}
            ],
        }
        if settings.filter_rule:
            search_query["rules"].append(settings.filter_rule.dict())

        self.entities = port_client.search_entities(search_query)
        self.scorecard = port_client.get_scorecard(
            settings.blueprint, settings.scorecard
        ).get("scorecard")
