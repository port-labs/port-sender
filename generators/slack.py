from typing import Dict, List, Any

import generators.base
import utils


class SlackMessageGenerator(generators.base.BaseMessageGenerator):

    def generate_scorecards_reminders(self,
                                      blueprint: str,
                                      scorecard: Dict[str, Any],
                                      entities: list) -> List[Dict[str, Any]]:
        blueprint_plural = utils.convert_to_plural(blueprint)
        entities_didnt_pass_gold_level = {
            "Basic": [],
            "Bronze": [],
            "Silver": [],
        }
        number_of_entities_didnt_pass_gold_level = 0
        for entity in entities:
            entity_scorecard_result = entity.get("scorecards", {}).get(scorecard.get("identifier"), {})
            number_of_rules = len(entity_scorecard_result.get("rules", []))
            if entity_scorecard_result.get("level") != "Gold":
                passed_rules = [rule for rule in entity_scorecard_result.get("rules", []) if rule.get("status") == "SUCCESS"] or []
                entities_didnt_pass_gold_level[entity_scorecard_result.get("level")].append(
                    {
                        "identifier": entity.get("identifier"),
                        "name": entity.get("title"),
                        "passed_rules": passed_rules,
                        "number_of_rules": number_of_rules
                    }
                )
                number_of_entities_didnt_pass_gold_level += 1

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
                        "text": f"*⚠️ {blueprint_plural} with unmet rules ({number_of_entities_didnt_pass_gold_level})*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self._generate_entities_list_with_level_and_link(blueprint,
                                                                                 entities_didnt_pass_gold_level)
                    }
                }
            ]
        return blocks

    @staticmethod
    def _generate_entities_list_with_level_and_link(blueprint: str,
                                                    entities_by_level: Dict[str, List[Dict[str, str]]]) -> str:
        text = ""
        base_entity_url = f"https://app.getport.io/{blueprint}Entity?identifier="
        for level, entities in entities_by_level.items():
            if not entities:
                continue
            text += f"*{level}*\n"
            for entity in entities:
                text += f"• <{base_entity_url}{entity.get('identifier')}|{entity.get('name')}>" \
                        f" [{len(entity.get('passed_rules'))}/{entity.get('number_of_rules')}] Passed \n"
        return text
