import contextlib

import boto3

from . import random_str


class TemporaryBucket:
    @staticmethod
    @contextlib.contextmanager
    def create():
        s3_resource = boto3.resource('s3')

        bucket_name = f'temp-bucket{random_str.make(8).lower()}'
        bucket = s3_resource.Bucket(bucket_name)

        bucket.create()

        try:
            yield bucket
        except Exception as e:
            raise e
        finally:
            clear(bucket)
            bucket.delete()


def clear(bucket):
    for obj in bucket.objects.all():
        print(obj)
        obj.delete()
