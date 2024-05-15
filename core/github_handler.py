import logging

from config import settings
from core.base_handler import BaseHandler
from generators.github import GithubIssueGenerator
from targets.github import Github

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GithubHandler(BaseHandler):
    def issue_handler(self):
        if not self.entities:
            logger.info("No entities found")
            return

        logger.info("Searching for Github issues to create / update")

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
                tasks = []
                # Iterating rules of scorecard level
                for rule in rules_by_level[level]:
                    full_rule_object = [
                        scorecard_rule
                        for scorecard_rule in self.scorecard.get("rules", [])
                        if scorecard_rule.get("identifier") == rule.get("identifier")
                    ][0]
                    task = GithubIssueGenerator().generate_task(full_rule_object)
                    rule_successful = rule.get("status", "") == "SUCCESS"
                    if rule_successful:
                        tasks.append(f"- [x] {task}")
                    elif not rule_successful:
                        tasks.append(f"- [ ] {task}")

                generated_issue = GithubIssueGenerator().generate_issue(
                    self.scorecard, entity, settings.blueprint, level, tasks
                )
                issue_search_result = Github().search_issue_by_labels(generated_issue["labels"])
                issue_search_result
                issue_exists = issue_search_result > 0

                if not issue_exists:
                    if scorecard_level_completed:
                        continue
                    Github().create_issue(generated_issue)
                else:
                    issue = issue_search_result[0]
                    # TODO: Find how to spot closed issue
                    if issue["state"]=='closed' and not scorecard_level_completed:
                        Github().reopen_issue(issue)

                if (
                    scorecard_level_completed
                    and issue_exists
                    # TODO: Find how to spot open issue
                    and not issue["fields"]["resolution"]["isClosed"]
                ):
                    Github().resolve_issue(issue)
