
import json

import events
import schedule


def scheduler(event):
    """
        Wrapper around scheduler lambda that can be imported by
        pytest correctly
    """
    new_granules = event['new_granules']

    print('Scheduling hyp3_jobs')
    print(json.dumps([g['name'] for g in new_granules]))
    job_packages = schedule.hyp3_jobs(new_granules)
    print('Found {} jobs to start'.format(len(job_packages)))

    print('Making notify only events')
    notify_only_events = events.make_notify_events(job_packages)

    print('Sending {} notify events'.format(len(notify_only_events)))
    print('Sending...')
    events.send(notify_only_events)
