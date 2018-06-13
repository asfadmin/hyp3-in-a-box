import collections

from .hyp3_event import Hyp3Event


class NotifyOnlyEvent(Hyp3Event, collections.namedtuple('NotiyOnlyData', [
    'address',
    'subject',
    'additional_info',
    'browse_url',
    'download_url',
    'unsubscribe_url'
])):
    """
        * subject - Email subject
        * additional_info - list of dict with more meta data about the event
            * name - Metadata title
            * value - Metadata content
        * browse_url - URL of a browse image to display
        * download_url - URL where the processed data can be downloaded from
        * unsubscribe_url - URL to disable email notifications of this type
    """
    pass
