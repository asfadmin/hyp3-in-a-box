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
        * **address** - Address to send email
        * **subject** - Email subject
        * **additional_info** - list of dict with meta data about the event
            * **name** - Metadata title
            * **value** - Metadata content
        * **browse_url** - URL of a browse image to display
        * **download_url** - URL where the processed data can be downloaded
        * **unsubscribe_url** - URL to disable email notifications
    """
    pass
