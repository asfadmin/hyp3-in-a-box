
import abc
import json


class Hyp3Event(abc.ABC):
    """ Base class for all hyp3 events"""

    @classmethod
    def from_json(cls, event_json):
        """ Constructor for making hyp3 events from json.

            :param str event_data: json representing the event
        """
        data = json.loads(event_json)

        return cls(**data)

    def to_json(self):
        """ Convert a hyp3 event to json.

            :returns: the hyp3 event in json form
            :rtype: str
        """
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def to_dict(self):
        """
            :returns: dictionary representing the event
            :rtype: dict
        """
        return NotImplemented

    @property
    @abc.abstractmethod
    def event_type(self):
        """
            :returns: the events type
            :rtype: str
        """
        return NotImplemented
