import boto3
import botocore
import pathlib as pl
from .environment import environment as env

s3 = boto3.resource('s3')


def download(path):
    """Try and download a file from s3

        :param key: str
    """
    key = pl.Path(path).name

    try:
        do_download(key, path)
    except botocore.exceptions.ClientError as e:
        raise handle_client_error(e, key)


def handle_client_error(e, key):
    if e.response['Error']['Code'] != "404":
        error_msg = get_no_object_error_msg(key)
        print(error_msg)

        return ObjectDoesntExist(error_msg)

    else:
        return e


def get_no_object_error_msg(key):
    return "S3 DOWNLOAD WARNING: The object {} does not exist.".format(
        key
    )


def do_download(key, path):
    """Make the boto3 call to download the file from s3

        :param key: str
    """
    s3.Bucket(env.bucket) \
        .download_file(key, path)


def upload(file_path):
    """Upload a file to s3 lambda bucket

        :param key: str

        :returns: s3.Object
    """
    key = pl.Path(file_path).name
    bucket = s3.Bucket(env.bucket)

    with open(file_path, 'rb') as f:
        return bucket.put_object(
            Key=key,
            Body=f
        )


class ObjectDoesntExist(Exception):
    pass
