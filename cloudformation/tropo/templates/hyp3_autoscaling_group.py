# hyp3_autoscaling_group.py
# Rohan Weeden
# Created: June 21, 2018

"""
Troposphere template responsible for creating the worker auto scaling group.
This group adds instances as more requests are added to the processing SQS
Queue.

Processing instances are configured through the userdata. The CloudFormation
adds the stack name to the userdata string, which sets the value as an
environment variable before restarting the hyp3 daemon service. All other
general configuration variables (e.g. queue name, sns arn, products bucket) are
stored in SSM Parameter Store and read by the instance on startup. The names of
these parameters are known ahead of time except for the stack name prefix, which
is supplied by the user data.

For the purposes of development, the userdata will checkout the latest
orchestration code from the hyp3-in-a-box dev branch before starting the hyp3
daemon. This makes testing changes a lot easier because it means no new AMI is
required, and no manual copying of files is needed. This "development mode" can
be enabled by setting the ``clone_in_userdata`` environment variable to ``True``
when generating the CloudFormation template.

Requires
~~~~~~~~
* :ref:`keypair_name_param_template`
* :ref:`vpc_template`

Resources
~~~~~~~~~

* **Auto Scaling Group:** The cluster of hyp3 processing instances.
* **Launch Configuration:** Instance definitions for the auto scaling group.
* **Security Group:** Firewall rules for processing instances.
* **Cloudwatch Alarm:** Created by the TargetTrackingScaling Policy.

"""


from troposphere import FindInMap, Parameter, Ref
from troposphere.autoscaling import (
    AutoScalingGroup,
    CustomizedMetricSpecification,
    LaunchConfiguration,
    ScalingPolicy,
    Tags,
    TargetTrackingConfiguration
)
from troposphere.ec2 import SecurityGroup, SecurityGroupRule

from template import t
from tropo_env import environment

from .ec2_userdata import user_data
from .hyp3_keypairname_param import keyname
from .hyp3_vpc import get_public_subnets, hyp3_vpc
from .utils import get_map

print('  adding auto scaling group')

custom_metric_name = "RTCJobsPerInstance"

max_instances = t.add_parameter(Parameter(
    "MaxRTCProcessingInstances",
    Description="The maximum RTC processing instances that can run concurrently.",
    Type="Number",
    Default=4
))

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

launch_config = t.add_resource(LaunchConfiguration(
    "Hyp3LaunchConfiguration",
    ImageId=FindInMap(
        "Region2AMI",
        Ref("AWS::Region"), "AMIId"
    ),
    KeyName=Ref(keyname),
    SecurityGroups=[Ref(security_group)],
    InstanceType="m1.small",
    UserData=user_data
))

processing_group = t.add_resource(AutoScalingGroup(
    "Hyp3AutoscalingGroup",
    LaunchConfigurationName=Ref(launch_config),
    MinSize=0,
    MaxSize=Ref(max_instances),
    VPCZoneIdentifier=[Ref(subnet) for subnet in get_public_subnets()],
    HealthCheckType="EC2",
    Tags=Tags(
        Maturity=environment.maturity,
        Project="hyp3-in-a-box",
        StackName=Ref('AWS::StackName'),
        Name="HyP3-Worker"
    )
))

target_tracking_scaling_policy = t.add_resource(ScalingPolicy(
    "HyP3ScaleByBackloggedMessages",
    AutoScalingGroupName=Ref(processing_group),
    PolicyType="TargetTrackingScaling",
    TargetTrackingConfiguration=TargetTrackingConfiguration(
        CustomizedMetricSpecification=CustomizedMetricSpecification(
            MetricName=custom_metric_name,
            Namespace=Ref('AWS::StackName'),
            Statistic="Average"
        ),
        DisableScaleIn=True,
        TargetValue=1.0  # Keep a ratio of 1 message per instance
    )
))
