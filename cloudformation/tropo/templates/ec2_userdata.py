from troposphere import Base64, Ref, Sub


_user_data = """#! /bin/bash
echo STACK_NAME=${StackName} > ~/env

systemctl restart hyp3
"""

user_data = Base64(
    Sub(
        _user_data,
        StackName=Ref('AWS::StackName')
    )
)
