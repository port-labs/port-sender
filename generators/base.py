import abc


class BaseMessageGenerator(abc.ABC):
    @abc.abstractmethod
    def scorecard_reminder(self, blueprint: str, scorecard_name: str, entities: list):
        pass

    @abc.abstractmethod
    def scorecard_report(self, blueprint: str, scorecard: str, entities: list):
        pass
