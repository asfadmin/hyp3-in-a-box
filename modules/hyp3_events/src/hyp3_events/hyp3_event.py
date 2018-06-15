
import abc
import json


class Hyp3Event(abc.ABC):
    @property
    @abc.abstractmethod
    def event_type(self):
        return NotImplemented

    @classmethod
    def from_json(cls, event_data):
        """Constructor for making hyp3 events from json."""
        data = json.loads(event_data)

        return cls(**data)

    @abc.abstractmethod
    def to_json(self):
        return NotImplemented

    @abc.abstractmethod
    def to_dict(self):
        return NotImplemented
