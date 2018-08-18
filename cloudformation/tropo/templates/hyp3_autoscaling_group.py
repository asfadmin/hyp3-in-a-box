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
these parameters are known ahead of time except for the stack name prefix,
which is supplied by the user data.

For the purposes of development, the :ref:`userdata_helper` will checkout the
latest orchestration code from the hyp3-in-a-box dev branch before starting the
hyp3 daemon. This makes testing changes a lot easier because it means no new AMI
is required, and no manual copying of files is needed. This "development mode"
can be enabled by setting the ``clone_in_userdata`` environment variable to
``True`` when generating the CloudFormation template.

Requires
~~~~~~~~
* :ref:`keypair_name_param_template`
* :ref:`vpc_template`
* :ref:`s3_template`
* :ref:`sns_template`
* :ref:`sqs_template`

Resources
~~~~~~~~~

* **Auto Scaling Group:** The cluster of hyp3 processing instances.
* **Launch Configuration:** Instance definitions for the auto scaling group.
* **Security Group:** Firewall rules for processing instances.
* **Cloudwatch Alarm:** Created by the TargetTrackingScaling Policy.
* **IAM Policies:**

  * Instance write permission on products bucket
  * Instance read permission on products bucket for generating presigned urls
  * Instance recieve and delete permissions on start events queue
  * Instance publish permission on finished events topic
  * Instance terminate permission on autoscaling group

"""

from awacs.autoscaling import TerminateInstanceInAutoScalingGroup
from awacs.aws import Allow, Policy, Statement
from awacs.s3 import GetObject, PutObject
from awacs.sns import Publish
from awacs.sqs import DeleteMessage, GetQueueUrl, ReceiveMessage
from awacs.ssm import GetParameter
from troposphere import FindInMap, GetAtt, Join, Parameter, Ref, Sub
from troposphere.autoscaling import (
    AutoScalingGroup,
    CustomizedMetricSpecification,
    LaunchConfiguration,
    ScalingPolicy,
    Tags,
    TargetTrackingConfiguration
)
from troposphere.ec2 import SecurityGroup, SecurityGroupRule
from troposphere.iam import InstanceProfile
from troposphere.iam import Policy as IAMPolicy
from troposphere.iam import PolicyType, Role

from template import t
from tropo_env import environment

from .ec2_userdata import user_data
from .hyp3_keypairname_param import keyname
from .hyp3_s3 import products_bucket
from .hyp3_sns import finish_sns
from .hyp3_sqs import start_events
from .hyp3_vpc import get_public_subnets, hyp3_vpc, net_gw_vpc_attachment
from .utils import get_ec2_assume_role_policy, get_map

print('  adding auto scaling group')

custom_metric_name = "RTCJobsPerInstance"

t.add_mapping("Region2Principal", get_map('region2principal'))

max_instances = t.add_parameter(Parameter(
    "MaxRTCProcessingInstances",
    Description="The maximum RTC processing instances that can run concurrently.",
    Type="Number",
    Default=4
))

instance_type = t.add_parameter(Parameter(
    "RTCProcessingInstanceType",
    Description="The type of EC2 instance to process with. Default is m5.xlarge",
    Type="String",
    Default="m5.xlarge"
))

spot_price = t.add_parameter(Parameter(
    "RTCProcessingSpotPrice",
    Description="The maximum price to pay for a spot instance. \
    Setting this value enables spot processing.",
    Type="Number"
))

t.add_mapping("Region2AMI", get_map('region2ami'))

security_group = t.add_resource(SecurityGroup(
    "Hyp3ProcessingInstancesSecurityGroup",
    GroupDescription="Allow ssh to processing instances",
    VpcId=Ref(hyp3_vpc),
    SecurityGroupIngress=[
        SecurityGroupRule(
            "HyP3ProcessingInstancesSecurityGroupSSHIn",
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp="0.0.0.0/0"
        )
    ],
    SecurityGroupEgress=[
        SecurityGroupRule(
            "HyP3ProcessingInstancesSecurityGroupWebOut",
            IpProtocol="tcp",
            FromPort="80",
            ToPort="80",
            CidrIp="0.0.0.0/0"
        ),
        SecurityGroupRule(
            "HyP3ProcessingInstancesSecurityGroupWebSOut",
            IpProtocol="tcp",
            FromPort="443",
            ToPort="443",
            CidrIp="0.0.0.0/0"
        )
    ]
))

products_bucket_access = IAMPolicy(
    PolicyName="ProductsPutObject",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[
                    GetObject,
                    PutObject
                ],
                Resource=[
                    Sub(
                        "${Arn}/*",
                        Arn=GetAtt(products_bucket, "Arn")
                    )
                ]
            )
        ]
    )
)

poll_messages = IAMPolicy(
    PolicyName="QueueGetMessages",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[
                    ReceiveMessage,
                    DeleteMessage,
                    GetQueueUrl
                ],
                Resource=[GetAtt(start_events, "Arn")]
            )
        ]
    )
)

publish_notifications = IAMPolicy(
    PolicyName="PublishNotifications",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[Publish],
                Resource=[Ref(finish_sns)]
            )
        ]
    )
)

get_parameter_resources = [
    Sub("arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/${AWS::StackName}/*")
]
if environment.clone_in_userdata:
    get_parameter_resources.append(
        Sub("arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/CodeBuild/GITHUB_HYP3_API_CLONE_TOKEN")
    )
get_parameters = IAMPolicy(
    PolicyName="GetParameters",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[GetParameter],
                Resource=get_parameter_resources
            )
        ]
    )
)

role = t.add_resource(Role(
    "HyP3WorkerRole",
    AssumeRolePolicyDocument=get_ec2_assume_role_policy(
        FindInMap("Region2Principal", Ref("AWS::Region"), "EC2Principal")
    ),
    Path="/",
    Policies=[
        products_bucket_access,
        poll_messages,
        publish_notifications,
        get_parameters
    ]
))

instance_profile = t.add_resource(InstanceProfile(
    "HyP3WorkerInstanceProfile",
    Path="/",
    Roles=[Ref(role)]
))

launch_config = t.add_resource(LaunchConfiguration(
    "HyP3LaunchConfiguration",
    ImageId=FindInMap(
        "Region2AMI",
        Ref("AWS::Region"), "AMIId"
    ),
    KeyName=Ref(keyname),
    SecurityGroups=[Ref(security_group)],
    InstanceType=Ref(instance_type),
    UserData=user_data,
    IamInstanceProfile=Ref(instance_profile),
    DependsOn=net_gw_vpc_attachment,
    SpotPrice=Ref(spot_price)
))

processing_group = t.add_resource(AutoScalingGroup(
    "HyP3AutoscalingGroup",
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

terminate_instance = t.add_resource(PolicyType(
    "HyP3InstanceTerminateSelf",
    PolicyName="TerminateSelf",
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[TerminateInstanceInAutoScalingGroup],
                Resource=[
                    Join(":", [
                        "arn",
                        "aws",
                        "autoscaling",
                        Ref("AWS::Region"),
                        Ref("AWS::AccountId"),
                        "autoScalingGroup",
                        "*",
                        Sub(
                            "autoScalingGroupName/${GroupName}",
                            GroupName=Ref(processing_group)
                        )
                    ])
                ]
            )
        ]
    ),
    Roles=[Ref(role)]
))
