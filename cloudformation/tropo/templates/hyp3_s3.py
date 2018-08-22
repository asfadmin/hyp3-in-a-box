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

products_bucket = t.add_resource(
    s3.Bucket(
        "S3Bucket",
        BucketName=Sub(
            "${StackName}-products-bucket",
            StackName=Ref("AWS::StackName")
        )
    )
)

ssm_products_bucket_name = t.add_resource(SSMParameter(
    "HyP3SSMParameterProductsBucket",
    Name=Sub(
        "/${StackName}/ProductsS3Bucket",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value=Ref(products_bucket)
))
