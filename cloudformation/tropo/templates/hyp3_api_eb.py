# hyp3_api_eb.py
# Rohan Weeden
# Created: May 24, 2018

# Troposphere definitions for the HyP3 API Elastic beanstalk application

# Converted from ElasticBeanstalk_Nodejs.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from awacs.aws import Action, Allow, Policy, Principal, Statement
from awacs.sts import AssumeRole
from template import t
from troposphere import FindInMap, GetAtt, Join, Output, Parameter, Ref
from troposphere.elasticbeanstalk import (
    Application,
    ApplicationVersion,
    ConfigurationTemplate,
    Environment,
    OptionSettings,
    SourceBundle
)
from troposphere.iam import InstanceProfile
from troposphere.iam import PolicyType as IAMPolicy
from troposphere.iam import Role

keyname = t.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH access to "
                "the AWS Elastic Beanstalk instance",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair."
))

t.add_mapping("Region2Principal", {
    'ap-northeast-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'ap-southeast-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'ap-southeast-2': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'cn-north-1': {
        'EC2Principal': 'ec2.amazonaws.com.cn',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com.cn'},
    'eu-central-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'eu-west-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'sa-east-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'us-east-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'us-west-1': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'},
    'us-west-2': {
        'EC2Principal': 'ec2.amazonaws.com',
        'OpsWorksPrincipal': 'opsworks.amazonaws.com'}
    }
)

t.add_resource(Role(
    "WebServerRole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow, Action=[AssumeRole],
                Principal=Principal(
                    "Service", [
                        FindInMap(
                            "Region2Principal",
                            Ref("AWS::Region"), "EC2Principal")
                    ]
                )
            )
        ]
    ),
    Path="/"
))

t.add_resource(IAMPolicy(
    "WebServerRolePolicy",
    PolicyName="WebServerRole",
    PolicyDocument=Policy(
        Statement=[
            Statement(Effect=Allow, NotAction=Action("iam", "*"),
                      Resource=["*"])
        ]
    ),
    Roles=[Ref("WebServerRole")]
))

role = t.add_resource(InstanceProfile(
    "WebServerInstanceProfile",
    Path="/",
    Roles=[Ref("WebServerRole")]
))

app = t.add_resource(Application(
    "Hyp3Api",
    ApplicationName="hyp3-api",
    Description="AWS Elastic Beanstalk API for interacting with the HyP3 system"
))

app_version = t.add_resource(ApplicationVersion(
    "Hyp3ApiTestVersion",
    Description="Version 1.0",
    ApplicationName=Ref(app),
    SourceBundle=SourceBundle(
        S3Bucket=Join("-", ["elasticbeanstalk-samples", Ref("AWS::Region")]),
        S3Key="python-sample-20150402.zip"
    )
))

config_template = t.add_resource(ConfigurationTemplate(
    "Hyp3ApiConfigurationTemplate",
    ApplicationName=Ref(app),
    Description="",
    SolutionStackName="64bit Amazon Linux 2015.03 v2.0.0 running Python 3.4",
    OptionSettings=[
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="EC2KeyName",
            Value=Ref(keyname)
        ),
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="IamInstanceProfile",
            Value=Ref(role)
        )
    ]
))

test_environment = t.add_resource(Environment(
    "Hyp3ApiTestEnvironment",
    Description="HyP3 API maturity: 'test'",
    ApplicationName=Ref(app),
    TemplateName=Ref(config_template),
    VersionLabel=Ref(app_version)
))

t.add_output(
    Output(
        "URL",
        Description="HyP3 API url",
        Value=Join("", ["http://", GetAtt(test_environment, "EndpointURL")])
    )
)
