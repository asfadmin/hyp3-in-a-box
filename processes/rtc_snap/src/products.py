import boto3

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')


def upload(*, paths, bucket_name):
    products_bucket = get_bucket(bucket_name)

    object_keys = [
        upload_from(path, products_bucket) for path in paths
    ]

    return [
        get_object_url(bucket_name, key) for key in object_keys
    ]


def upload_from(path, bucket):
    key = path.name

    with path.open('rb') as f:
        bucket.put_object(
            Key=key,
            Body=f
        )

    return key


def get_bucket(bucket_name):
    return s3_resource.Bucket(bucket_name)


def get_object_url(bucket, key):
    return f'{s3_client.meta.endpoint_url}/{bucket}/{key}'
