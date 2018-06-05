import boto3
import botocore

s3 = boto3.resource('s3')
LAMBDA_BUCKET = 'hyp3-in-a-box-lambdas'


def download(key):
    """Try and download a file from s3

        :param key: str
    """
    try:
        dl(key)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("S3 DOWNLOAD: The object {} does not exist.".format(key))
        else:
            raise


def dl(key):
    """Make the boto3 call to download the file from s3

        :param key: str

    """
    s3.Bucket(LAMBDA_BUCKET) \
        .download_file(key, key)


def upload(key):
    """Upload a file to s3 lambda bucket

        :param key: str

        :returns: s3.Object
    """
    bucket = s3.Bucket(LAMBDA_BUCKET)

    with open(key, 'rb') as f:
        return bucket.put_object(
            Key=key,
            Body=f
        )
