import logging

from config import settings, TargetKind
from port.client import PortClient
from targets import Slack, Jira
from generators import SlackMessageGenerator, JiraIssueGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Handler:
    @classmethod
    def scorecard_reminder(cls):
        logger.info("Initializing Port client")
        port_client = PortClient(settings.port_region, settings.port_client_id, settings.port_client_secret)
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
            blocks = SlackMessageGenerator().scorecard_reminder(settings.blueprint,
                                                                           scorecard,
                                                                           entities)
            logger.info("Sending scorecards reminders to slack channel")
            Slack().send_message(blocks)

    @classmethod
    def scorecard_report(cls):
        logger.info("Initializing Port client")
        port_client = PortClient(settings.port_region, settings.port_client_id, settings.port_client_secret)
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
            blocks = SlackMessageGenerator().scorecard_report(settings.blueprint,
                                                                       scorecard,
                                                                       entities)
            logger.info("Sending scorecard report to slack channel")
            Slack().send_message(blocks)

    @classmethod
    def ticket_handler(cls):
        logger.info("Initializing Port client")
        port_client = PortClient(settings.port_region, settings.port_client_id, settings.port_client_secret)
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
        if settings.target_kind == TargetKind.jira:
            logger.info(f"Generating scorecards tickets for {len(entities)} entities")

            for entity in entities:
                entity_scorecard = entity.get("scorecards", {}).get(scorecard.get("identifier"), {})
                rules_by_level = {
                    "Gold": [],
                    "Silver": [],
                    "Bronze": []
                }

                # Grouping rules by levels
                for rule in entity_scorecard.get("rules", []):
                    rules_by_level[rule.get("level")].append(rule)

                for level in rules_by_level:
                    scorecard_level_completed = all(rule.get("status", "") == "SUCCESS"
                                                       for rule in rules_by_level[level])

                    generated_task = JiraIssueGenerator().generate_task(scorecard,
                                                                        entity,
                                                                        settings.blueprint,
                                                                        level)
                    task_summary = generated_task["fields"]["summary"]
                    task_search_query = f"project={settings.jira_project_id} " \
                                        f"AND summary~'{task_summary}' " \
                                        f"AND issuetype = Task " \
                                        f"AND resolution is EMPTY " \
                                        f"ORDER BY created DESC"
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
                        full_rule_object = [scorecard_rule for scorecard_rule in scorecard.get("rules", [])
                                            if scorecard_rule.get("identifier") == rule.get("identifier")][0]
                        generated_subtask = JiraIssueGenerator().generate_subtask(full_rule_object,
                                                                                scorecard.get("title", ""),
                                                                                entity, parent_key)
                        subtask_search_query = f"project={settings.jira_project_id} " \
                                               f"AND summary~'{generated_subtask['fields']['summary']}' " \
                                               f"AND issuetype = Subtask " \
                                               f"AND resolution is EMPTY " \
                                               f"ORDER BY created DESC" \
                                               f""
                        rule_search_result = Jira().search_issue(subtask_search_query)
                        subtask_exists = rule_search_result["total"] > 0
                        if rule.get("status", "") == "SUCCESS":
                            if subtask_exists:
                                Jira().resolve_issue(rule_search_result["issues"][0]["key"],
                                                     settings.jira_resolve_transition_id)
                        else:
                            level_rules_completed = False
                            if not subtask_exists:
                                Jira().create_issue(generated_subtask)

                    if level_rules_completed and task_exists:
                        Jira().resolve_issue(parent_key, settings.jira_resolve_transition_id)

