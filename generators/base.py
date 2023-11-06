import abc


class BaseMessageGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_scorecards_reminders(self, blueprint: str, scorecard_name: str, entities: list):
        pass
