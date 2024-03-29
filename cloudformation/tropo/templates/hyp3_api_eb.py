# hyp3_api_eb.py
# Rohan Weeden, William Horn
# Created: May 24, 2018

"""
Troposphere definitions for the HyP3 API Elastic beanstalk application.

Converted from ElasticBeanstalk_Nodejs.template located at:
http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

Requires
~~~~~~~~
* :ref:`db_params_template`
* :ref:`keypair_name_param_template`
* :ref:`rds_template`
* :ref:`vpc_template`

Resources
~~~~~~~~~

* **ElasticBeanstalk:** Python 3.6 web server
* **IAM Policies:**

  * ElasticBeanstalk Web Tier

"""

from troposphere import FindInMap, GetAtt, Join, Output, Parameter, Ref, Sub
from troposphere.elasticbeanstalk import (
    Application,
    ApplicationVersion,
    ConfigurationTemplate,
    Environment,
    OptionSettings,
    SourceBundle
)
from troposphere.iam import InstanceProfile, Role

from template import t
from tropo_env import environment

from .hyp3_db_params import db_name, db_pass, db_user
from .hyp3_keypairname_param import keyname
from .hyp3_rds import hyp3_db
from .hyp3_vpc import public_net_1, hyp3_vpc
from .utils import get_ec2_assume_role_policy, get_map, make_s3_key

source_zip = "hyp3_api.zip"


print('  adding api_eb')

t.add_mapping("Region2Principal", get_map('region2principal'))

solution_stack_name = t.add_parameter(Parameter(
    "SolutionStackName",
    Description="ElasticBeanstalk configuration to run the API in. This should \
    be set to the latest version of the Python 3.6 container.",
    Type="String",
    Default="64bit Amazon Linux 2018.03 v2.7.3 running Python 3.6"
))

role = t.add_resource(Role(
    "HyP3ApiWebServerRole",
    AssumeRolePolicyDocument=get_ec2_assume_role_policy(
        FindInMap("Region2Principal", Ref("AWS::Region"), "EC2Principal")
    ),
    Path="/",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier"
    ]
))

instance_profile = t.add_resource(InstanceProfile(
    "WebServerInstanceProfile",
    Path="/",
    Roles=[Ref(role)]
))

app = t.add_resource(Application(
    "HyP3Api",
    ApplicationName=Sub(
        "${StackName}-hyp3-api",
        StackName=Ref('AWS::StackName')
    ),
    Description=("AWS Elastic Beanstalk API for "
                 "interacting with the HyP3 system")
))

app_version = t.add_resource(ApplicationVersion(
    "HyP3ApiTestVersion",
    Description="Version 1.0",
    ApplicationName=Ref(app),
    SourceBundle=SourceBundle(
        S3Bucket=environment.source_bucket,
        S3Key=make_s3_key(source_zip)
    )
))

config_template = t.add_resource(ConfigurationTemplate(
    "HyP3ApiConfigurationTemplate",
    DependsOn=[hyp3_vpc, hyp3_db],
    ApplicationName=Ref(app),
    Description="",
    SolutionStackName=Ref(solution_stack_name),
    OptionSettings=[
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="EC2KeyName",
            Value=Ref(keyname)
        ),
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="IamInstanceProfile",
            Value=Ref(instance_profile)
        ),
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="InstanceType",
            Value="t2.micro"
        ),
        OptionSettings(
            Namespace="aws:ec2:vpc",
            OptionName="VPCId",
            Value=Ref(hyp3_vpc)
        ),
        OptionSettings(
            Namespace="aws:ec2:vpc",
            OptionName="AssociatePublicIpAddress",
            Value="true"
        ),
        OptionSettings(
            Namespace="aws:ec2:vpc",
            OptionName="ELBScheme",
            Value="public"
        ),
        OptionSettings(
            Namespace="aws:ec2:vpc",
            OptionName="ELBSubnets",
            Value=Ref(public_net_1)
        ),
        OptionSettings(
            Namespace="aws:ec2:vpc",
            OptionName="Subnets",
            Value=Ref(public_net_1)
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="DB_URL",
            Value=GetAtt(hyp3_db, "Endpoint.Address")
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="DB_PORT",
            Value="5432"
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="DB_NAME",
            Value=Ref(db_name)
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="DB_USER",
            Value=Ref(db_user)
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="DB_PASS",
            Value=Ref(db_pass)
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="OAUTH_CONSUMER_KEY",
            Value='dummy-val'
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="OAUTH_CONSUMER_SECRET",
            Value='dummy-val'
        ),
        OptionSettings(
            Namespace="aws:elasticbeanstalk:application:environment",
            OptionName="OAUTH_PASSWORD",
            Value='dummy-val'
        )
    ]
))

eb_environment = t.add_resource(Environment(
    "HyP3ApiEnvironment",
    EnvironmentName=Sub(
        "${StackName}-${Maturity}",
        StackName=Ref('AWS::StackName'),
        Maturity=environment.maturity
    ),
    Description="HyP3 API maturity: '{}'".format(
        environment.maturity
    ),
    ApplicationName=Ref(app),
    TemplateName=Ref(config_template),
    VersionLabel=Ref(app_version)
))

api_url = Join("", ["http://", GetAtt(eb_environment, "EndpointURL")])
t.add_output(
    Output(
        "HyP3ApiUrl",
        Description="HyP3 API url",
        Value=api_url
    )
)
