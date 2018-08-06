# email_event.py
# Rohan Weeden
# Created: August 2, 2018

# Data structure for serializing the important contents of hyp3 emails.


import collections

from .hyp3_event import Hyp3Event

EmailData = collections.namedtuple('EmailData', [
    'user_id',
    'sub_id',
    'additional_info',
    'granule_name',
    'browse_url',
    'download_url',
])


class EmailEvent(EmailData, Hyp3Event):
    """
        * **user_id** - User id to send email to
        * **sub_id** - Subscription which
        * **additional_info** - list of dict with meta data about the event
            * **name** - Metadata title
            * **value** - Metadata content
        * **browse_url** - URL of a browse image to display
        * **download_url** - URL where the processed data can be downloaded
    """
    @property
    def event_type(self):
        return 'Hyp3EmailEvent'

    def to_dict(self):
        return self._asdict()
