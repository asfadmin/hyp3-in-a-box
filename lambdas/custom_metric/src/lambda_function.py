import boto3
import os

sqs_client = boto3.client("sqs")
asg_client = boto3.client("autoscaling")
cw_client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    """ Entry point for the lambda to run. Polls an SQS queue for unread messages
        and an AutoScalingGroup for number of active instances. It then updates
        a custom metric with the proportion of unread messages to active instances.

        :param event: lambda event data
            * QueueUrl - Which queue to describe
            * AutoScalingGroupName - Which ASG to describe
            * MetricName - Which metric to update
        :param context: lambda runtime info
    """
    print("Got event: {}".format(event))

    queue_url = event['QueueUrl']
    ag_name = event['AutoScalingGroupName']
    stack_name = os.environ['Hyp3StackName']

    num_messages = get_num_messages(queue_url)
    num_instances = get_num_instances(ag_name)

    print("Number of messages: ", num_messages)
    print("Number of running instances: ", num_instances)

    messages_per_instance = calculate_metric(num_messages, num_instances)

    print("Current number of messages per instance: ", messages_per_instance)

    cw_client.put_metric_data(
        Namespace=stack_name,
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
