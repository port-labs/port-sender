import abc
from typing import Any, Dict

class BaseIssueGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_issue(self, scorecard: Dict[str, Any], entity: Dict[str, Any], blueprint: str, level: str, tasks: list[str]):
        pass

    @abc.abstractmethod
    def generate_task(self, rule: Dict[str, Any]) -> str:
        pass

class BaseMessageGenerator(abc.ABC):
    @abc.abstractmethod
    def scorecard_reminder(self, blueprint: str, scorecard_name: str, entities: list):
        pass

    @abc.abstractmethod
    def scorecard_report(self, blueprint: str, scorecard: str, entities: list):
        pass


class BaseTicketGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_task(self, scorecard: Dict[str, Any], entity: Dict[str, Any], blueprint: str, level: str):
        pass

    @abc.abstractmethod
    def generate_subtask(self, rule: Dict[str, Any], scorecard_title: str, entity: Dict[str, Any], parent_key: str):
        pass
