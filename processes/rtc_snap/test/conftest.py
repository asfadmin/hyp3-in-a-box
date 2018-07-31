import boto3
import pytest


@pytest.fixture()
def testing_bucket():
    s3 = boto3.client('s3')

    bucket_name = 'hyp3-in-a-box-testing-bucket'
    response = s3.list_buckets()

    buckets = [bucket['Name'] for bucket in response['Buckets']]

    if bucket_name not in buckets:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'us-west-2'
            }
        )

    return bucket_name
