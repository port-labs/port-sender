from typing import Any, Dict, List

import generators.base
import utils
from config import settings
from port.utils import get_port_url


class SlackMessageGenerator(generators.base.BaseMessageGenerator):

    def scorecard_report(self, blueprint: str, scorecard: Dict[str, Any], entities: list):
        blueprint_plural = utils.convert_to_plural(blueprint).title()
        entities_by_level = {
            "Gold": [],
            "Silver": [],
            "Bronze": [],
            "Basic": [],
        }
        overall_entities_per_team = {}
        gold_entities_per_team = {}
        number_of_passed_entities_per_rule = {}
        for entity in entities:
            entity_scorecard_result = entity.get("scorecards", {}).get(scorecard.get("identifier"), {})
            entities_by_level[entity_scorecard_result.get("level")].append(
                {
                    "identifier": entity.get("identifier"),
                    "name": entity.get("title"),
                }
            )
            for team in entity.get("team", []):
                overall_entities_per_team[team] = overall_entities_per_team.get(team, 0) + 1
                if entity_scorecard_result.get("level") == "Gold":
                    gold_entities_per_team[team] = gold_entities_per_team.get(team, 0) + 1

            for rule in entity_scorecard_result.get("rules", []):
                number_of_passed_entities_per_rule[rule.get("identifier")] = \
                    number_of_passed_entities_per_rule.get(rule.get("identifier"), 0) + \
                    (1 if rule.get("status") == "SUCCESS" else 0)

        number_of_passed_entities_per_rules_by_title = {
            rule.get("title"): number_of_passed_entities_per_rule.get(rule.get("identifier"), 0)
            for rule in scorecard.get("rules", [])
        }

        top_highest_rules, top_lowest_rules = self._resolve_top_highest_lowest_scored_rules(
            entities, number_of_passed_entities_per_rules_by_title
        )
        top_teams = self._calculate_top_teams_by_percentage(entities, overall_entities_per_team)

        entities_by_level_text = ""
        for level, entities in entities_by_level.items():
            if not entities:
                continue
            entities_by_level_text += f"• {level} - {len(entities)} \n"

        top_teams_text = ""
        for team, percentage in top_teams:
            top_teams_text += f"• {team} - {percentage} \n"

        top_highest_scored_rules_text = ""
        for rule, percentage in top_highest_rules:
            top_highest_scored_rules_text += f"• {rule} - {percentage} \n"

        top_lowest_scored_rules_text = ""
        for rule, percentage in top_lowest_rules:
            top_lowest_scored_rules_text += f"• {rule} - {percentage} \n"

        scorecard_title = scorecard.get("title")
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📝 {scorecard_title} overview  report",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Here is a summary of the current {scorecard_title} scorecard status ⭐️"
                }
            },
        ]
        if entities_by_level_text:
            blocks += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*:vertical_traffic_light: {blueprint_plural} by level*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": entities_by_level_text
                    }
                }]
        else:
            blocks += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*:vertical_traffic_light: {blueprint_plural} by level*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "There are no entities with scorecard data :disappointed:"
                    }
                }
            ]
        if top_teams_text:
            blocks += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*:chart_with_upwards_trend: Top teams*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": top_teams_text
                    }
                },
            ]
        if top_highest_scored_rules_text:
            blocks += [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*:white_check_mark: Highest scoring rules*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": top_highest_scored_rules_text
                    }
                }
            ]
        if top_lowest_scored_rules_text:
            blocks += [

                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*:warning: Lowest scoring rules*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": top_lowest_scored_rules_text
                    }
                },
            ]
        blocks += [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Visit <{get_port_url(settings.port_region, 'app')}|Port> for more information."
                }
            }
        ]
        return blocks

    def scorecard_reminder(self,
                           blueprint: str,
                           scorecard: Dict[str, Any],
                           entities: list) -> List[Dict[str, Any]]:
        blueprint_plural = utils.convert_to_plural(blueprint).title()
        entities_didnt_pass_all_rules = {
            "Silver": [],
            "Bronze": [],
            "Basic": [],
        }
        number_of_entities_didnt_pass_all_rules = 0
        for entity in entities:
            entity_scorecard_result = entity.get("scorecards", {}).get(scorecard.get("identifier"), {})
            number_of_rules = len(entity_scorecard_result.get("rules", []))
            if entity_scorecard_result.get("level") != "Gold":
                passed_rules = [rule for rule in entity_scorecard_result.get("rules", []) if rule.get("status") == "SUCCESS"] or []
                if len(passed_rules) < number_of_rules:
                    entities_didnt_pass_all_rules[entity_scorecard_result.get("level")].append(
                        {
                            "identifier": entity.get("identifier"),
                            "name": entity.get("title"),
                            "passed_rules": passed_rules,
                            "number_of_rules": number_of_rules
                        }
                    )
                    number_of_entities_didnt_pass_all_rules += 1

        entities_didnt_pass_gold_level_sorted = {
            level: sorted(entities, key=lambda item: len(item.get("passed_rules", [])), reverse=True)
            for level, entities in entities_didnt_pass_all_rules.items()
        }

        blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":bell: {scorecard.get('title')} reminder",
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"This is a reminder that some of your {blueprint_plural} have unmet rules.\n Click "
                                f"on the links below to see how to improve the score of your {blueprint_plural} ⭐️"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*⚠️ {number_of_entities_didnt_pass_all_rules} {blueprint_plural} with unmet rules*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self._generate_entities_list_with_level_and_link(blueprint,
                                                                                 entities_didnt_pass_gold_level_sorted)
                    }
                }
            ]
        return blocks

    @staticmethod
    def _resolve_top_highest_lowest_scored_rules(entities: list,
                                                 number_of_passed_entities_per_rule: Dict[str, int]):
        """
        Get the top 3 highest and lowest scored rules by percentage
        If there are less than 3 rules, return all of them
        If there is rule that also in the top 3 highest and lowest, return it only in the highest
        Return the top 3 ordered by percentage in descending order
        :param entities:
        :param number_of_passed_entities_per_rule:
        :return:
        """

        top_3_highest_scored_rules = sorted(number_of_passed_entities_per_rule.items(),
                                            key=lambda item: item[1],
                                            reverse=True)[:3]

        top_3_lowest_scored_rules = sorted(number_of_passed_entities_per_rule.items(),
                                           key=lambda item: item[1],
                                           reverse=True)[-3:]

        top_3_highest_scored_rules_by_percentage = [
            (rule, f"{(number_of_passed_entities_per_rule.get(rule, 0) / len(entities)) * 100:.2f}%")
            for rule, _ in top_3_highest_scored_rules
        ]

        top_3_lowest_scored_rules_by_percentage = [
            (rule, f"{(number_of_passed_entities_per_rule.get(rule, 0) / len(entities)) * 100:.2f}%")
            for rule, _ in top_3_lowest_scored_rules
        ]

        filtered_top_lowest_scored_rules_by_percentage = []
        for lowest_rule, value in top_3_lowest_scored_rules_by_percentage:
            matched = False
            for highest_rule, _ in top_3_highest_scored_rules_by_percentage:
                if highest_rule == lowest_rule:
                    matched = True
                    break
            if not matched:
                filtered_top_lowest_scored_rules_by_percentage.append((lowest_rule, value))

        return top_3_highest_scored_rules_by_percentage, filtered_top_lowest_scored_rules_by_percentage

    @staticmethod
    def _calculate_top_teams_by_percentage(entities: list,
                                           entities_by_team: Dict[str, int]):
        """
        Calculate the top 3 teams by percentage
        :param entities:
        :param entities_by_team:
        :return:
        """
        top_3_teams_by_percentage = [
            (team, f"{(entities_by_team.get(team, 0) / len(entities)) * 100:.2f}%")
            for team, _ in sorted(entities_by_team.items(), key=lambda item: item[1], reverse=True)[:3]
        ]
        return top_3_teams_by_percentage

    @staticmethod
    def _generate_entities_list_with_level_and_link(blueprint: str,
                                                    entities_by_level: Dict[str, List[Dict[str, str]]]) -> str:
        text = ""
        base_entity_url = f"{get_port_url(settings.port_region, 'app')}/{blueprint}Entity?identifier="
        for level, entities in entities_by_level.items():
            if not entities:
                continue

            text += f"\n*{level}*\n\n"
            for entity in entities:
                text += f"• <{base_entity_url}{entity.get('identifier')}|{entity.get('name')}>" \
                        f" - `[{len(entity.get('passed_rules'))}/{entity.get('number_of_rules')}] Passed` \n"
        return text
