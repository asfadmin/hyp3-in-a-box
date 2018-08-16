from typing import NamedTuple, Union

from hyp3_events import NewGranuleEvent, StartEvent, EmailEvent
from hyp3_db.hyp3_models import Subscription, User, Process


class Job(NamedTuple):
    """ All the required information for scheduling and creating a HyP3 job """

    sub: Subscription
    """ A subscription overlapping the granule"""
    process: Process
    """ The process for the subscription"""
    user: User
    """ The user who the subscritpion belongs to"""
    granule: NewGranuleEvent
    """ A new granule to schedule a job for"""

    def to_event(self) -> Union[EmailEvent, StartEvent]:
        """ Convert the job into a hyp3_event object"""
        if self._is_notify_only():
            return self._to_email_event()

        return self._to_start_event()

    def _is_notify_only(self) -> bool:
        return 'notify' in self.process.name.lower()

    def _to_start_event(self) -> StartEvent:
        return StartEvent(
            granule=self.granule.name,
            user_id=self.user.id,
            sub_id=self.sub.id,
            output_patterns=self.process.output_patterns,
            script_path=self.process.script,
            additional_info=[]
        )

    def _to_email_event(self) -> EmailEvent:
        return EmailEvent(
            user_id=self.user.id,
            sub_id=self.sub.id,
            additional_info=[],
            browse_url=self.granule.browse_url,
            download_url=self.granule.download_url,
            granule_name=self.granule.name
        )
