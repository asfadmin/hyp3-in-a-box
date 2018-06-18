import collections
import json

from .hyp3_event import Hyp3Event

NotifyOnlyData = collections.namedtuple('NotiyOnlyData', [
    'address',
    'subject',
    'additional_info',
    'browse_url',
    'download_url',
])


class NotifyOnlyEvent(NotifyOnlyData, Hyp3Event):
    """
        * **address** - Address to send email
        * **subject** - Email subject
        * **additional_info** - list of dict with meta data about the event
            * **name** - Metadata title
            * **value** - Metadata content
        * **browse_url** - URL of a browse image to display
        * **download_url** - URL where the processed data can be downloaded
    """
    @property
    def event_type(self):
        return 'Hyp3NotifyOnlyEvent'

    def to_dict(self):
        return self._asdict()
