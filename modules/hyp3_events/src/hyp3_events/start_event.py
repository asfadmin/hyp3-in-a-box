from .hyp3_event import Hyp3Event


class StartEvent(Hyp3Event):
    @property
    def event_type(self):
        return 'Hyp3NewGranuleEvent'

    def to_dict(self):
        return {}
