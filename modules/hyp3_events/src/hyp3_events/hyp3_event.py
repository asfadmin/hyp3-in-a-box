
import json


class Hyp3Event():
    @classmethod
    def from_json(cls, event_data):
        """Constructor for making hyp3 events from json."""
        data = json.loads(event_data)

        return cls(**data)

    def to_json(self):
        """Convert a hyp3 event to json."""
        return json.dump(self.__dict__)
