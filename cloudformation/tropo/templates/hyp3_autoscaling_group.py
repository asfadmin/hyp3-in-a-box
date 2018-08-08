# hyp3_autoscaling_group.py
# Rohan Weeden
# Created: June 21, 2018

"""
Troposphere template responsible for creating the worker auto scaling group.
This group adds instances as more requests are added to the processing SQS
Queue.

Requires
~~~~~~~~
* :ref:`sqs_template`
* :ref:`vpc_template`

Resources
~~~~~~~~~

* **Auto Scaling Group:** The cluster of hyp3 processing instances.
* **Launch Configuration:** Instance definitions for the auto scaling group.
* **Security Group:** Firewall rules for processing instances.
* **Cloudwatch Alarm:** Triggers the auto scaling group to increase instance count.

"""

from template import t
from tropo_env import environment
from troposphere import Base64, FindInMap, Ref, Sub
from troposphere.autoscaling import (
    AutoScalingGroup,
    LaunchConfiguration,
    ScalingPolicy,
    Tags
)
from troposphere.cloudwatch import Alarm, MetricDimension
from troposphere.ec2 import SecurityGroup, SecurityGroupRule

from .hyp3_keypairname_param import keyname
from .hyp3_sqs import start_events
from .hyp3_vpc import get_public_subnets, hyp3_vpc
from .utils import get_map

print('  adding auto scaling group')

t.add_mapping("Region2AMI", get_map('region2ami'))


security_group = t.add_resource(SecurityGroup(
    "Hyp3ProcessingInstancesSecurityGroup",
    GroupDescription="Allow ssh to processing instances",
    VpcId=Ref(hyp3_vpc),
    SecurityGroupIngress=[
        SecurityGroupRule(
            "Hyp3ProcessingInstancesSecurityGroupSSHIn",
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp="0.0.0.0/0"
        )
    ],
    SecurityGroupEgress=[
        SecurityGroupRule(
            "Hyp3ProcessingInstancesSecurityGroupWebOut",
            IpProtocol="tcp",
            FromPort="80",
            ToPort="80",
            CidrIp="0.0.0.0/0"
        )
    ]
))

user_data = """#! /bin/bash
echo STACK_NAME=${StackName} > ~/env

systemctl restart hyp3
"""
launch_config = t.add_resource(LaunchConfiguration(
    "Hyp3LaunchConfiguration",
    ImageId=FindInMap(
        "Region2AMI",
        Ref("AWS::Region"), "AMIId"
    ),
    KeyName=Ref(keyname),
    SecurityGroups=[Ref(security_group)],
    InstanceType="m1.small",
    UserData=Base64(
        Sub(
            user_data,
            StackName=Ref('AWS::StackName')
        )
    )
))

processing_group = t.add_resource(AutoScalingGroup(
    "Hyp3AutoscalingGroup",
    LaunchConfigurationName=Ref(launch_config),
    MinSize=0,  # Hardcoded for now
    MaxSize=4,  # Hardcoded for now
    VPCZoneIdentifier=[Ref(subnet) for subnet in get_public_subnets()],
    HealthCheckType="EC2",
    Tags=Tags(
        Maturity=environment.maturity,
        Project="hyp3-in-a-box",
        StackName=Ref('AWS::StackName'),
        Name="HIB-Worker"
    )
))

add_instance_scaling_policy = t.add_resource(ScalingPolicy(
    "Hyp3ScaleOutPolicy",
    AutoScalingGroupName=Ref(processing_group),
    PolicyType="SimpleScaling",
    ScalingAdjustment=1,
    AdjustmentType="ChangeInCapacity"
))


def add_alarm(name, description, threshold, period_seconds):
    return t.add_resource(Alarm(
        name,
        AlarmActions=[Ref(add_instance_scaling_policy)],
        ActionsEnabled=True,
        AlarmDescription=description,
        Dimensions=[
            MetricDimension(
                Name="QueueName",
                Value=Ref(start_events)
            )
        ],
        MetricName="ApproximateNumberOfMessagesVisible",
        Statistic="Maximum",
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Threshold="{}".format(threshold),
        EvaluationPeriods=1,
        Namespace="AWS/SQS",
        Period=period_seconds
    ))


add_instance_alarm_1 = add_alarm(
    "Hyp3ScaleUpAlarmFirst",
    "Start processing when the first job comes in",
    threshold=1,
    period_seconds=10
)

add_instance_alarm = add_alarm(
    "Hyp3ScaleUpAlarm",
    "When more hyp3 processing instances are required",
    threshold=4,
    period_seconds=60
)
