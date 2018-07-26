import collections

from .hyp3_event import Hyp3Event

RTCSnapJobData = collections.namedtuple('Hyp3ProcessStartData', [
    'granule',
    'address',
    'username',
    'subscription',
    'output_file_patterns'
])


class RTCSnapJob(RTCSnapJobData, Hyp3Event):
    @property
    def event_type(self):
        return 'Hyp3RTCSnapJob'

    def to_dict(self):
        return self._asdict()
