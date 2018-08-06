import collections

from .hyp3_event import Hyp3Event

StartEventData = collections.namedtuple('Hyp3ProcessStartData', [
    'granule',
    'address',
    'username',
    'subscription',
    'output_patterns',
    'script_path'
])


class StartEvent(StartEventData, Hyp3Event):
    @property
    def event_type(self):
        return 'Hyp3StartEvent'

    def to_dict(self):
        return self._asdict()
