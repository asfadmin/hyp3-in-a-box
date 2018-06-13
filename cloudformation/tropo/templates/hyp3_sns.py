
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
            Endpoint=GetAtt(send_email, "Arn"),
            DependsOn=Ref(send_email)
        )
    ]
))

sns_invoke_permissions = t.add_resource(Permission(
    "SNSSchedulerInvokePermissions",
    FunctionName=Ref(send_email),
    Action="lambda:InvokeFunction",
    Principal="sns.amazonaws.com",
    SourceArn=GetAtt(finish_sns, "Arn")
))
