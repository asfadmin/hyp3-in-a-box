# hyp3_kms_key.py
# Rohan Weeden
# Created: June 13, 2018

# AWS Encryption key used to keep sensitive HyP3 credentials secure.

from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from troposphere import AWS_ACCOUNT_ID, Join, Ref, kms

from template import t

print('  adding KMS key')


key_policy = PolicyDocument(
    Version="2012-10-17",
    Statement=[
        Statement(
            Sid="1",
            Effect=Allow,
            Principal=Principal(
                "AWS", [
                    Join(":", ["arn:aws:iam", Ref(AWS_ACCOUNT_ID)])
                ]
            ),
            Action=[Action("kms", "*")],
            Resource=["*"]
        )
    ]
)

kms_key = t.add_resource(
    kms.Key(
        "Hyp3KMSKey",
        Description="KMS Key used by HyP3 to encrypt sensitive data",
        KeyPolicy=key_policy
    )
)
