import collections

from .hyp3_event import Hyp3Event


NewGranuleData = collections.namedtuple('NewGranuleData', [
    'name',
    'polygon',
    'download_url'
])


class NewGranuleEvent(NewGranuleData, Hyp3Event):
    """
        * **name** - Name of the granule
        * **polygon** - Polygon representing the area of the granule
        * **download_url** - URL where the granule can be downloaded
    """
    @property
    def event_type(self):
        return 'Hyp3NewGranuleEvent'

    def to_dict(self):
        return self._asdict()