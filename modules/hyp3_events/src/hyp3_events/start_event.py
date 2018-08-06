import collections

from .hyp3_event import Hyp3Event

StartEventData = collections.namedtuple('StartEventData', [
    'granule',
    'user_id',
    'sub_id',
    'output_patterns',
    'script_path',
    'additional_info'
])


class StartEvent(StartEventData, Hyp3Event):
    def to_dict(self):
        return self._asdict()
