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
from troposphere import FindInMap, Ref, Sub, Base64
from troposphere.autoscaling import (
    AutoScalingGroup,
    LaunchConfiguration,
    ScalingPolicy
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

sudo systemctl restart hyp3
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
    HealthCheckType="EC2"
))

add_instance_scaling_policy = t.add_resource(ScalingPolicy(
    "Hyp3ScaleInPolicy",
    AutoScalingGroupName=Ref(processing_group),
    PolicyType="SimpleScaling",
    ScalingAdjustment=1,
    AdjustmentType="ChangeInCapacity"
))

add_instance_alarm = t.add_resource(Alarm(
    "Hyp3ScaleUpAlarm",
    AlarmActions=[Ref(add_instance_scaling_policy)],
    ActionsEnabled=True,
    AlarmDescription="When more hyp3 processing instances are required",
    Dimensions=[
        MetricDimension(
            Name="QueueName",
            Value=Ref(start_events)
        )
    ],
    MetricName="ApproximateNumberOfMessagesVisible",
    Statistic="Maximum",
    ComparisonOperator="GreaterThanOrEqualToThreshold",
    Threshold="4",
    EvaluationPeriods=1,
    Namespace="AWS/SQS",
    Period=60 * 5,  # 5 minutes
))
