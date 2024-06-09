from typing import Dict, Type
import logging

from config import settings
from core.base_handler import BaseHandler
from core.jira_handler import JiraHandler
from core.github_handler import GithubHandler
from core.slack_handler import SlackHandler

HANDLERS: Dict[str, Type[BaseHandler]] = {
    "jira": JiraHandler,
    "slack": SlackHandler,
    "github": GithubHandler
}

if len(logging.getLogger().handlers) > 0:
    # The Lambda environment pre-configures a handler logging to stderr.
    # If a handler is already configured, `.basicConfig` does not execute.
    # Thus we set the level directly.
    # https://stackoverflow.com/a/56579088
    logging.getLogger().setLevel(settings.log_level)
else:
    logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    operation_kind = settings.operation_kind
    handler = HANDLERS.get(settings.target_kind, SlackHandler)()
    operation_kind_handler = getattr(handler, settings.operation_kind)
    operation_kind_handler()
