from typing import Dict, List, Any

import generators.base
from config import settings

scorecards_singular_operators = ["isEmpty", "isNotEmpty"]


class JiraIssueGenerator(generators.base.BaseTicketGenerator):

    def generate_task(self, scorecard: Dict[str, Any], entity: Dict[str, Any], blueprint: str, level: str):
        scorecard_title = scorecard.get("title", "")
        entity_title = entity.get("title", "")

        return {
                    "fields": {
                            "project": {
                                "key": settings.jira_project_id
                            },
                            "summary": f"{scorecard_title} tasks to reach the {level} level "
                                       f"for the {blueprint}: {entity.get('identifier', '')}",
                            "description": {
                                "version": 1,
                                "type": "doc",
                                "content": [
                                    {
                                        "type": "heading",
                                        "attrs": {
                                            "level": 2
                                        },
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": f"⭐️ {scorecard_title} tasks for the {blueprint}: {entity_title} "
                                            }
                                        ]
                                    },
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "This task contains all sub-tasks needed to be completed for "
                                            },
                                            {
                                                "type": "text",
                                                "text": entity_title,
                                                "marks": [
                                                    {
                                                        "type": "link",
                                                        "attrs": {
                                                            "href": f'https://app.getport.io/appEntity?identifier={entity.get("identifier")}'
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "text",
                                                "text": " to reach the "
                                            },
                                            {
                                                "type": "text",
                                                "text": level,
                                                "marks": [
                                                    {
                                                        "type": "strong"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "text",
                                                "text": f" level in the {scorecard_title} scorecard."
                                            }
                                        ]
                                    },
                                    {
                                        "type": "paragraph",
                                        "content": []
                                    },
                                    {
                                        "type": "panel",
                                        "attrs": {
                                            "panelType": "note"
                                        },
                                        "content": [
                                            {
                                                "type": "paragraph",
                                                "content": [
                                                    {
                                                        "type": "text",
                                                        "text": "Scorecards",
                                                        "marks": [
                                                            {
                                                                "type": "strong"
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": " are a way for you and your team to define and track standards, metrics, and KPIs in different categories such as production readiness, quality, productivity, and more."
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "paragraph",
                                                "content": [
                                                    {
                                                        "type": "text",
                                                        "text": "For more information about your scorecards, go to "
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": "Port",
                                                        "marks": [
                                                            {
                                                                "type": "link",
                                                                "attrs": {
                                                                    "href": "http://app.getport.io"
                                                                }
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "type": "text",
                                                        "text": "."
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            "issuetype": {
                                "name": "Task"
                            }
                        }
        }

    def generate_subtask(self, rule: Dict[str, Any], scorecard_title: str, entity: Dict[str, Any], parent_key: str):
        rule_title = rule.get("title", "")
        query = rule.get("query", "")
        conditions_for_display = JiraIssueGenerator._generate_conditions(query.get("conditions", []),
                                                                         query.get("combinator", ""))
        return {
            "fields": {
                "parent": {"key": parent_key},
                "project": {
                    "key": settings.jira_project_id
                },
                "summary": f"{rule_title} ({rule.get('identifier', '')})",
                "issuetype": {
                    "name": "Subtask"
                },
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"This {scorecard_title} {rule_title} rule is currently not passed for "
                                },
                                {
                                    "type": "text",
                                    "text": entity.get("title"),
                                    "marks": [
                                        {
                                            "type": "link",
                                            "attrs": {
                                                "href": f'https://app.getport.io/appEntity?'
                                                        f'identifier={entity.get("identifier")}'
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "text",
                                    "text": ". To pass it,"
                                            " you need to meet the following rule conditions:"
                                }
                            ]
                        },
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": " "
                                }
                            ]
                        },
                        {
                            "type": "expand",
                            "attrs": {
                                "title": f"{rule_title} conditions"
                            },
                            "content": conditions_for_display
                        },
                        {
                            "type": "paragraph",
                            "content": []
                        },
                        {
                            "type": "panel",
                            "attrs": {
                                "panelType": "note"
                            },
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Scorecards",
                                            "marks": [
                                                {
                                                    "type": "strong"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "text",
                                            "text": " are a way for you and your team to define and "
                                                    "track standards, metrics, and KPIs in different"
                                                    " categories such as production readiness, "
                                                    "quality, productivity, and more."
                                        }
                                    ]
                                },
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "For more information about your scorecards, go to "
                                        },
                                        {
                                            "type": "text",
                                            "text": "Port",
                                            "marks": [
                                                {
                                                    "type": "link",
                                                    "attrs": {
                                                        "href": "http://app.getport.io"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "type": "text",
                                            "text": "."
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

    @staticmethod
    def _generate_conditions(conditions: List[Dict[str, Any]], combinator: str):
        conditions_for_display = []
        for index, condition in enumerate(conditions):
            port_property = condition.get("property", "")
            operator = condition.get("operator", "")
            rule_prefix = "When" if index == 0 else combinator
            expression = ""
            if operator in scorecards_singular_operators:
                expression = f"Is {port_property} {operator}"
            else:
                expression = f"{port_property} {operator} {condition.get('value')}"

            condition_paragraph = {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"{rule_prefix} ",
                        "marks": [
                            {
                                "type": "code"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": expression
                    }
                ]
            }

            conditions_for_display.append(condition_paragraph)

        return conditions_for_display
