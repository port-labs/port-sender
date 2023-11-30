import logging

from config import settings
from generators.jira import JiraIssueGenerator
from targets.jira import Jira

from core.base_handler import BaseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JiraHandler(BaseHandler):
    def ticket_handler(self):
        if not self.entities:
            logger.info("No entities found")
            return

        logger.info(
            f"Generating scorecards tickets for" f" {len(self.entities)} entities"
        )

        for entity in self.entities:
            entity_scorecard = entity.get("scorecards", {}).get(
                self.scorecard.get("identifier"), {}
            )
            rules_by_level = {"Gold": [], "Silver": [], "Bronze": []}

            # Grouping rules by levels
            for rule in entity_scorecard.get("rules", []):
                rules_by_level[rule.get("level")].append(rule)

            for level in rules_by_level:
                scorecard_level_completed = all(
                    rule.get("status", "") == "SUCCESS"
                    for rule in rules_by_level[level]
                )

                generated_task = JiraIssueGenerator().generate_task(
                    self.scorecard, entity, settings.blueprint, level
                )
                task_summary = generated_task["fields"]["summary"]
                task_search_query = (
                    f"project={settings.jira_project_id} "
                    f"AND summary~'{task_summary}' "
                    f"AND issuetype = Task "
                    f"AND resolution is EMPTY "
                    f"ORDER BY created DESC"
                )
                task_search_result = Jira().search_issue(task_search_query)
                level_rules_completed = True
                task_exists = task_search_result["total"] > 0
                if not task_exists:
                    if scorecard_level_completed:
                        continue
                    logger.info("Issue doesn't exist, creating issue")
                    response = Jira().create_issue(generated_task)
                    parent_key = response["key"]
                else:
                    parent_key = task_search_result["issues"][0]["key"]

                for rule in rules_by_level[level]:
                    full_rule_object = [
                        scorecard_rule
                        for scorecard_rule in self.scorecard.get("rules", [])
                        if scorecard_rule.get("identifier") == rule.get("identifier")
                    ][0]
                    generated_subtask = JiraIssueGenerator().generate_subtask(
                        full_rule_object,
                        self.scorecard.get("title", ""),
                        entity,
                        parent_key,
                    )
                    subtask_search_query = (
                        f"project={settings.jira_project_id} "
                        f"AND summary~'{generated_subtask['fields']['summary']}' "
                        f"AND issuetype = Subtask "
                        f"AND resolution is EMPTY "
                        f"AND parent = '{parent_key}'"
                    )
                    rule_search_result = Jira().search_issue(subtask_search_query)
                    subtask_exists = rule_search_result["total"] > 0

                    if rule.get("status", "") == "SUCCESS":
                        if subtask_exists:
                            Jira().resolve_issue(
                                rule_search_result["issues"][0]["key"]
                            )
                    else:
                        level_rules_completed = False
                        if not subtask_exists:
                            Jira().create_issue(generated_subtask)

                if level_rules_completed and task_exists:
                    Jira().resolve_issue(
                        parent_key
                    )
