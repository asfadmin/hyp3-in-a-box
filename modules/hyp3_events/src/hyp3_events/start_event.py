import collections

from .hyp3_event import Hyp3Event

StartEventData = collections.namedtuple('StartEventData', [
    'granule',
    'address',
    'username',
    'subscription',
    'output_patterns',
    'script_path'
])


class StartEvent(StartEventData, Hyp3Event):
    def to_dict(self):
        return self._asdict()
