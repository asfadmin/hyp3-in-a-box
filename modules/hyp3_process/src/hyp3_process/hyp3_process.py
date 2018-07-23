from . import sqs


def process(queue, event_type):
    job = sqs.poll(queue, event_type)
    job.delete()

    return job
