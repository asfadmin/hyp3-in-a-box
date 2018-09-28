from typing import Dict
import json
import boto3
# from .NewEvent_to_StartEvent import make_dispatchable
import make_dispatchable

def scheduler(aws_event: Dict) -> None:
    """ Wrapper around scheduler lambda that can be imported by pytest."""
    new_granule_events = events.make_new_granule_events_with(
        aws_event['new_granules']
    )

    new_hyp3_events = make_dispatchable()

    # jobs = schedule.hyp3_jobs(new_granule_events)
    #
    # new_hyp3_events = events.make_from(jobs)

    # send hyp3_events to the dispatcher
    boto3.client('lambda').invoke(
        FunctionName=scheduler.environment.dispatch_lambda,
        InvocationType='Event',
        Payload=json.dump(new_hyp3_events.to_dict())
    )


    # def to_event(event: Hyp3Event) -> Union[EmailEvent, StartEvent]:
    #     """ Convert the job into a hyp3_event object"""
    #     if event._is_notify_only():
    #         return self._to_email_event()
    #
    #     return self._to_start_event()
    #
    # def _is_notify_only(self) -> bool:
    #     return 'notify' in self.process.name.lower()
    #
    # def _to_start_event(self) -> StartEvent:
    #     return StartEvent(
    #         granule=self.granule.name,
    #         user_id=self.user.id,
    #         sub_id=self.sub.id,
    #         output_patterns=self.process.output_patterns,
    #         script_path=self.process.script,
    #         additional_info=[]
    #     )
    #
    # def _to_email_event(self) -> EmailEvent:
    #     return EmailEvent(
    #         status='Success',
    #         user_id=self.user.id,
    #         sub_id=self.sub.id,
    #         additional_info=[],
    #         browse_url=self.granule.browse_url,
    #         download_url=self.granule.download_url,
    #         granule_name=self.granule.name
    #     )