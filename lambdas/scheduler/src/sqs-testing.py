import boto3
import random

START_EVENTS_QUEUE_NAME = 'test-fifo-sqs-Hyp3StartEvents-12P29WTQD29UU.fifo'
sqs = boto3.resource('sqs')


def get_start_events_queue():
    return sqs.get_queue_by_name(QueueName=START_EVENTS_QUEUE_NAME)


def queue_event():
    q = get_start_events_queue()

    body = f'Start Event Here, ID: {random.randint(0, 100)}'
    m = q.send_message(
        MessageBody=body,
        MessageGroupId="777"
    )

    print(f"sent message: {m.get('MessageId')}")


def get_events():
    q = get_start_events_queue()
    messages = q.receive_messages(
        AttributeNames=['MessageGroupId'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    for message in messages:
        print(message.body)
        message.delete()


def add():
    for _ in range(10):
        queue_event()


if __name__ == "__main__":
    get_events()
