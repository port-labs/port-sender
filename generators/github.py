from typing import Any, Dict
import generators.base
from port.utils import get_port_url
from config import settings


class GithubIssueGenerator(generators.base.BaseIssueGenerator):
    def generate_issue(
        self,
        scorecard: Dict[str, Any],
        entity: Dict[str, Any],
        blueprint: str,
        level: str,
        tasks: list[str],
    ):
        scorecard_title = scorecard.get("title", "")
        entity_title = entity.get("title", "")
        return {
            "title": f"{scorecard_title} tasks to reach the {level} level for the {blueprint}: {entity.get('identifier', '')}",
            "body": f"⭐️ {scorecard_title} tasks for the {blueprint}: {entity_title} \n"
            f"This issue contains all sub-tasks needed to be completed for [{entity_title}](https://app.getport.io/appEntity?identifier={entity.get('identifier')}) to reach the {level} level in the {scorecard_title} scorecard.\n"
            f"\n> :bulb: **Tip:** Scorecards are a way for you and your team to define and track standards, metrics, and KPIs in different categories such as production readiness, quality, productivity, and more. For more information about your scorecards, go to [Port]({get_port_url(settings.port_region)})"
            "\n# Tasks"
            "\n" + "\n".join(tasks) + "\n",
            "labels": ["Port", scorecard_title, level],
        }

    def generate_task(self, rule: dict[str, Any]):
        return f"{rule.get('title', '')} ({rule.get('identifier', '')})"
