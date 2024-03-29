# hyp3_kms_key.py
# Rohan Weeden
# Created: June 13, 2018

"""
Troposphere template responsible for generating AWS Encryption key used to keep
sensitive HyP3 credentials secure.

Resources
~~~~~~~~~

* **KMS Key:** A new KMS key
* **IAM Policies:**

  * Full management permissions by root account
"""

from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from template import t
from troposphere import AWS_ACCOUNT_ID, Join, Ref, kms

print('  adding KMS key')


key_policy = PolicyDocument(
    Version="2012-10-17",
    Statement=[
        Statement(
            Sid="1",
            Effect=Allow,
            Principal=Principal(
                "AWS", Join(":", ["arn:aws:iam:", Ref(AWS_ACCOUNT_ID), "root"])
            ),
            Action=[Action("kms", "*")],
            Resource=["*"]
        )
    ]
)

kms_key = t.add_resource(
    kms.Key(
        "HyP3KMSKey",
        Description="KMS Key used by HyP3 to encrypt sensitive data",
        KeyPolicy=key_policy
    )
)
