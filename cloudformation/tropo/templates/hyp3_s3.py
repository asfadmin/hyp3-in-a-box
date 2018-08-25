"""
Troposphere template responsible for the product bucket

Resources
~~~~~~~~~

* **S3 Bucket:** Where all the hyp3 products are stored
* **SSM Parameter:** Stores the name of the products bucket

"""
from troposphere import s3, Sub, Ref
from troposphere.ssm import Parameter as SSMParameter

from template import t

products_bucket = t.add_resource(s3.Bucket(
    "ProductsBucket",

    LifecycleConfiguration=s3.LifecycleConfiguration(Rules=[
        s3.LifecycleRule(
            Id="S3BucketRule001",
            Prefix="/products",
            Status="Enabled",
            Transitions=[
                s3.LifecycleRuleTransition(
                    StorageClass="STANDARD_IA",
                    TransitionInDays=30,
                )
            ],
        ),
    ]),

))

ssm_products_bucket_name = t.add_resource(SSMParameter(
    "HyP3SSMParameterProductsBucket",
    Name=Sub(
        "/${StackName}/ProductsS3Bucket",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value=Ref(products_bucket)
))
