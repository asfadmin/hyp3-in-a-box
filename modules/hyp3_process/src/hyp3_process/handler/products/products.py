import pathlib as pl

from typing import List

import boto3

from ..outputs import ProcessOutputs

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

PRODUCTS_DIR = "products"
BROWSE_DIR = "browse"


def upload(*, outputs: ProcessOutputs, bucket_name: str) -> List[str]:
    print(f'uploading products to {bucket_name}')
    products_bucket = get_bucket(bucket_name)

    archive_key, browse_key = [
        upload_from(outputs.archive, products_bucket, prefix=PRODUCTS_DIR),
        upload_from(outputs.browse, products_bucket, prefix=BROWSE_DIR)
    ]

    return [
        get_object_url(bucket_name, key) for key in (archive_key, browse_key)
    ]


def upload_from(path: pl.Path, bucket, prefix: str) -> str:
    key = str(pl.Path(prefix) / path.name)

    with path.open('rb') as f:
        bucket.put_object(
            Key=key,
            Body=f
        )

    return key


def get_bucket(bucket_name: str):
    return s3_resource.Bucket(bucket_name)


def get_object_url(bucket, key: str) -> str:
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        },
        ExpiresIn=604800
    )
    return url
