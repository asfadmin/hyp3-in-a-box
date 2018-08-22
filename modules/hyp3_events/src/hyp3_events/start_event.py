import collections

from .hyp3_event import HyP3Event

StartEventData = collections.namedtuple('StartEventData', [
    'granule',
    'user_id',
    'sub_id',
    'output_patterns',
    'script_path',
    'additional_info'
])


class StartEvent(StartEventData, HyP3Event):
    def to_dict(self):
        return self._asdict()
