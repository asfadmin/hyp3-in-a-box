import os

import boto3

from target_calculation import calculate_metric

sqs_client = boto3.client("sqs")
asg_client = boto3.client("autoscaling")
cw_client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    """ Entry point for the lambda to run. Polls an SQS queue for unread messages
        and an AutoScalingGroup for number of active instances. It then updates
        a custom metric with the proportion of unread messages to active
        instances.

        :param event: lambda event data

            * QueueUrl - Which queue to describe
            * AutoScalingGroupName - Which ASG to describe
            * MetricName - Which metric to update

        :param context: lambda runtime info
    """
    print("Got event: {}".format(event))

    queue_url = event['QueueUrl']
    ag_name = event['AutoScalingGroupName']
    metric_name = event['MetricName']
    stack_name = os.environ['HyP3StackName']

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
                'MetricName': metric_name,
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

    return len(active_only(response['AutoScalingGroups'][0]['Instances']))


def active_only(instances):
    return list(
        filter(
            lambda instance: instance['LifecycleState'] == 'InService',
            instances
        )
    )
