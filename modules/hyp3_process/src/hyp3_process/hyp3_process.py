from . import sqs


def process(event_type):
    event = sqs.poll(event_type)

    return event
