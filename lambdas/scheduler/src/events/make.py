from typing import Any, Dict, List

from hyp3_events import EmailEvent, Hyp3Event, NewGranuleEvent, StartEvent

from schedule import Job


# Add some conversion functions on the EmailEvent type
def email_event_from_type(obj: Any) -> EmailEvent:
    if isinstance(obj, Job):
        return email_event_from_job(obj)
    raise NotImplemented("from_type not implemented for {}".format(type(obj)))


def email_event_from_job(job: Job) -> EmailEvent:
    """ Converts a Job to an EmailEvent.

        :returns: A new EmailEvent object
        :rtype: EmailEvent
    """
    (sub, user, granule) = job
    return EmailEvent(
        user_id=user.id,
        sub_id=sub.id,
        additional_info=[],
        browse_url=granule.browse_url,
        download_url=granule.download_url,
        granule_name=granule.name
    )


setattr(EmailEvent, 'from_type', email_event_from_type)


def make_new_granule_events_with(new_granule_dicts: List[Dict[str, Any]]) -> List[NewGranuleEvent]:
    events = [
        NewGranuleEvent(**event)
        for event in new_granule_dicts
    ]

    return events


def make_from(jobs: List[Job]) -> List[Hyp3Event]:
    """ make email packages into notify only events

        :param list(tuple): email packages of the form schedule.Job(sub, user, granule)

        :returns: hyp3 events corresponding to each package
        :rtype: list[hyp3_events.EmailEvent]
    """
    events = [_make_event(job) for job in jobs]

    return events


def _make_event(job: Job) -> Hyp3Event:
    if job.sub.process_id == 1:
        return EmailEvent.from_type(job)

    return StartEvent()
