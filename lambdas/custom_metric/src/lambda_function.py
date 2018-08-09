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

    resp = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=[
            'ApproximateNumberOfMessages'
        ]
    )
    num_messages = int(resp['Attributes']['ApproximateNumberOfMessages'])

    # TODO: Paginate?
    response = asg_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            ag_name,
        ],
        MaxRecords=100
    )

    num_instances = len(
        list(
            filter(
                lambda x: x['LifecycleState'] == 'InService',
                response['AutoScalingGroups'][0]['Instances']
            )
        )
    )

    print("Number of messages: ", num_messages)
    print("Number of running instances: ", num_instances)

    if num_instances == 0:
        # Something kindof arbitrary, but still greater than having 1 instance
        messages_per_instance = num_messages * 2
    else:
        messages_per_instance = num_messages / num_instances

    print("Current number of messages per instance: ", messages_per_instance)

    response = cw_client.put_metric_data(
        Namespace=STACK_NAME,
        MetricData=[
            {
                'MetricName': 'MessagesPerInstance',
                'Value': messages_per_instance
            },
        ]
    )
