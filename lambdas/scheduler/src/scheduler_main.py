
import json

import events
import schedule


def scheduler(event):
    new_granules = event['new_granules']

    print('Scheduling hyp3_jobs')
    print(json.dumps([g['name'] for g in new_granules]))
    job_packages = schedule.hyp3_jobs(new_granules)
    print(f'Found {len(job_packages)} jobs to start')

    print('Making notify only events')
    notify_only_events = events.make_notify_events(job_packages)

    print(f'Sending {len(notify_only_events)} notify events')
    print('Sending...')
    events.send(notify_only_events)
