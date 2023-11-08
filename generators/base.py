import abc


class BaseMessageGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_scorecards_reminders(self, blueprint: str, scorecard_name: str, entities: list):
        pass

    @abc.abstractmethod
    def generate_scorecard_report(self, blueprint: str, scorecard: str, entities: list):
        pass
