import pathlib as pl

import boto3
import botocore

from .find_new_env import environment as env

s3 = boto3.resource('s3')


def download(path):
    """ Try and download a file from s3

        :param str path: path of object to download
    """
    key = pl.Path(path).name

    try:
        do_download(key, path)
    except botocore.exceptions.ClientError as e:
        raise get_correct_exception(e, key)


def get_correct_exception(e, key):
    if e.response['Error']['Code'] != "404":
        error_msg = get_no_object_error_msg(key)
        print(error_msg)

        return ObjectDoesntExist(error_msg)

    return e


def get_no_object_error_msg(key):
    return "S3 DOWNLOAD WARNING: The object {} does not exist.".format(
        key
    )


def do_download(key, path_to_download):
    s3.Bucket(env.bucket) \
        .download_file(key, path_to_download)


def upload(file_path):
    """ Upload a file to s3 lambda bucket

        :param str file_path: path of file to upload

        :rtype: s3.Object
        :returns: object of the uploaded file
    """
    key = pl.Path(file_path).name
    bucket = s3.Bucket(env.bucket)

    with open(file_path, 'rb') as f:
        return bucket.put_object(
            Key=key,
            Body=f
        )


class ObjectDoesntExist(Exception):
    """ Thrown when a key doesn't exist in s3"""
    pass
