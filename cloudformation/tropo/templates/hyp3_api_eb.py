# hyp3_api_eb.py
# Rohan Weeden
# Created: May 24, 2018

# Troposphere definitions for the HyP3 API Elastic beanstalk application

# Converted from ElasticBeanstalk_Nodejs.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from template import disable_title_validation, t
from troposphere import GetAtt, Join, Output, Parameter, Ref
from troposphere.elasticbeanstalk import (
    Application,
    ApplicationVersion,
    ConfigurationTemplate,
    Environment,
    OptionSettings,
    SourceBundle
)

disable_title_validation(Application)
disable_title_validation(ApplicationVersion)
disable_title_validation(ConfigurationTemplate)

t.add_version()

t.add_description(
    "AWS CloudFormation Sample Template ElasticBeanstalk_Nodejs_Sample: "
    "Configure and launch the AWS Elastic Beanstalk sample application. "
    "**WARNING** This template creates one or more Amazon EC2 instances. You "
    "will be billed for the AWS resources used if you create a stack from "
    "this template.")

keyname = t.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH access to "
                "the AWS Elastic Beanstalk instance",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair."
))

app = t.add_resource(Application(
    "hyp3-api",
    Description="AWS Elastic Beanstalk API for interacting with the HyP3 system"
))

app_version = t.add_resource(ApplicationVersion(
    "hyp3-api-test-0",
    Description="Version 1.0",
    ApplicationName=Ref(app),
    SourceBundle=SourceBundle(
        S3Bucket=Join("-", ["elasticbeanstalk-samples", Ref("AWS::Region")]),
        S3Key="python-sample-20150402.zip"
    )
))

config_template = t.add_resource(ConfigurationTemplate(
    "hyp3-api-configuration-template",
    ApplicationName=Ref(app),
    Description="",
    SolutionStackName="Python 3.4 running on 64bit Amazon Linux/2.7.0",
    OptionSettings=[
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="EC2KeyName",
            Value=Ref(keyname)
        ),
        OptionSettings(
            Namespace="aws:autoscaling:launchconfiguration",
            OptionName="IamInstanceProfile",
            Value=Ref("aws-elasticbeanstalk-ec2-role")
        )
    ]
))

test_environment = t.add_resource(Environment(
    "test",
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
