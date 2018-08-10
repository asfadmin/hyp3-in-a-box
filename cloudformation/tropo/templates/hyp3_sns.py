# hyp3_sns.py
# William Horn
# Created: June, 2018

"""
Requires
~~~~~~~~
* :ref:`send_email_template`

Resources
~~~~~~~~~

* **SNS Topic:**
* **SSM Parameter FinishEventSNSArn:** Contains the ARN of the Topic
* **Iam:**

    * Permission for Topic to trigger send_email
"""

from template import t
from troposphere import GetAtt, Ref, Sub
from troposphere.awslambda import Permission
from troposphere.sns import Subscription, Topic
from troposphere.ssm import Parameter

from .hyp3_send_email import send_email

print('  adding sns')

finish_sns = t.add_resource(Topic(
    "Hyp3FinishEventSNSTopic",
    Subscription=[
        Subscription(
            Protocol="lambda",
            Endpoint=GetAtt(send_email, "Arn")
        )
    ]
))

sns_invoke_permissions = t.add_resource(Permission(
    "SNSSchedulerInvokePermissions",
    Action="lambda:InvokeFunction",
    Principal="sns.amazonaws.com",
    SourceArn=Ref(finish_sns),
    FunctionName=GetAtt(send_email, "Arn")
))

ssm_sns_arn = t.add_resource(Parameter(
    "Hyp3SSMParameterFinishEventSNSArn",
    Name=Sub(
        "/${StackName}/FinishEventSNSArn",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value=Ref(finish_sns)
))
