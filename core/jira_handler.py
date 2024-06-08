import logging

from config import settings
from core.base_handler import BaseHandler
from generators.jira import JiraIssueGenerator
from targets.jira import Jira

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JiraHandler(BaseHandler):
    def ticket_handler(self):
        if not self.entities:
            logger.info("No entities found")
            return

        logger.info("Searching for Jira issues to create / update")

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
                    f"ORDER BY created DESC"
                )
                task_search_result = Jira().search_issue(task_search_query)

                task_exists = task_search_result["total"] > 0

                if not task_exists:
                    if scorecard_level_completed:
                        continue
                    parent_key = Jira().create_issue(generated_task)["key"]
                else:
                    task = task_search_result["issues"][0]
                    parent_key = task["key"]
                    if (task["fields"]["resolution"] and
                            not scorecard_level_completed):
                        Jira().reopen_issue(task)

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
                        f"AND parent = '{parent_key}'"
                    )
                    rule_search_result = Jira().search_issue(subtask_search_query)
                    rule_successful = rule.get("status", "") == "SUCCESS"

                    if rule_search_result["total"] > 0:
                        subtask = rule_search_result.get("issues", [])[0]
                        if rule_successful and not subtask["fields"]["resolution"]:
                            Jira().resolve_issue(subtask)
                        elif not rule_successful and subtask["fields"]["resolution"]:
                            Jira().reopen_issue(subtask)
                    elif not rule_successful:
                        logger.info(
                            f"Creating subtask for {rule.get('title')} in {parent_key} for {entity.get('name')}")
                        Jira().create_issue(generated_subtask)

                if (scorecard_level_completed and
                        task_exists and not task["fields"]["resolution"]):
                    Jira().resolve_issue(task)
