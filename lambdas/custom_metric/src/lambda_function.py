import boto3
import os

sqs_client = boto3.client("sqs")
asg_client = boto3.client("autoscaling")
cw_client = boto3.client('cloudwatch')

STACK_NAME = os.environ['Hyp3StackName']


def lambda_handler(event, context):
    print("Got event: {}".format(event))

    queue_url = event['QueueUrl']
    ag_name = event['AutoScalingGroupName']

    num_messages = get_num_messages(queue_url)
    num_instances = get_num_instances(ag_name)

    print("Number of messages: ", num_messages)
    print("Number of running instances: ", num_instances)

    messages_per_instance = calculate_metric(num_messages, num_instances)

    print("Current number of messages per instance: ", messages_per_instance)

    cw_client.put_metric_data(
        Namespace=STACK_NAME,
        MetricData=[
            {
                'MetricName': 'MessagesPerInstance',
                'Value': messages_per_instance
            },
        ]
    )


def get_num_messages(queue_url):
    resp = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=[
            'ApproximateNumberOfMessages'
        ]
    )
    return int(resp['Attributes']['ApproximateNumberOfMessages'])


def get_num_instances(group_name):
    # TODO: Paginate?
    response = asg_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            group_name,
        ],
        MaxRecords=100
    )

    return len(filter_active_only(response['AutoScalingGroups'][0]['Instances']))


def filter_active_only(instances):
    return list(
        filter(
            lambda x: x['LifecycleState'] == 'InService',
            instances
        )
    )


def calculate_metric(num_messages, num_instances):
    if num_instances == 0:
        # Something kindof arbitrary, but still greater than having 1 instance
        return num_messages * 2

    return num_messages / num_instances
