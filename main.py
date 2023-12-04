from core.jira_handler import JiraHandler
from core.slack_handler import SlackHandler
from core.base_handler import BaseHandler
from config import settings

from typing import Dict, Type

HANDLERS: Dict[str, Type[BaseHandler]] = {
   "jira": JiraHandler,
   "slack": SlackHandler
}

if __name__ == '__main__':
    operation_kind = settings.operation_kind
    handler = HANDLERS.get(settings.target_kind, SlackHandler)()
    operation_kind_handler = getattr(handler, settings.operation_kind)
    operation_kind_handler()
