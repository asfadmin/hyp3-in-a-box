
import json

import dispatch
import events
import schedule


def scheduler(event):
    """ Wrapper around scheduler lambda that can be imported by pytest."""
    granules = event['new_granules']
    new_granule_events = events.make_new_granule_events_with(granules)

    print('Scheduling hyp3_jobs')
    print(json.dumps([g.name for g in new_granule_events]))

    job_packages = schedule.hyp3_jobs(new_granule_events)

    print('Found {} jobs to start'.format(len(job_packages)))
    print('Making notify only events')

    new_hyp3_events = events.make_from(job_packages)

    print('Sending {} new events'.format(len(new_hyp3_events)))

    dispatch.new_events(new_hyp3_events)

    print('Done!')
