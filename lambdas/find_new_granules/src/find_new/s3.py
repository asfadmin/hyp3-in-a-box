import boto3
import botocore
import pathlib as pl

s3 = boto3.resource('s3')
LAMBDA_BUCKET = 'hyp3-in-a-box-lambdas'


def download(key):
    """Try and download a file from s3

        :param key: str
    """
    try:
        dl(key)
    except botocore.exceptions.ClientError as e:
        handle_client_error(e, key)


def handle_client_error(e, key):
    if e.response['Error']['Code'] == "404":
        error_msg = get_no_object_error_msg(key)
        print(error_msg)
    else:
        raise


def get_no_object_error_msg(key):
    return "S3 DOWNLOAD WARNING: The object {} does not exist.".format(
        key
    )


def dl(key):
    """Make the boto3 call to download the file from s3

        :param key: str
    """
    s3.Bucket(LAMBDA_BUCKET) \
        .download_file(key, key)


def upload(file_path):
    """Upload a file to s3 lambda bucket

        :param key: str

        :returns: s3.Object
    """
    key = pl.Pathlib(file_path).name
    bucket = s3.Bucket(LAMBDA_BUCKET)

    with open(key, 'rb') as f:
        return bucket.put_object(
            Key=key,
            Body=f
        )
