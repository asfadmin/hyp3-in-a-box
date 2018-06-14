
from template import t

from troposphere import GetAtt, Ref
from troposphere.sns import Topic, Subscription
from troposphere.awslambda import Permission

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
