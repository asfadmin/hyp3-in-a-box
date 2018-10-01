import os
import boto3

import pytest

import import_tempaws
from tempaws import TemporaryBucket


def test_tempbucket(s3file):
    with TemporaryBucket.create() as bucket:
        bucket.upload_file(s3file, 'test.txt')
        assert bucket.objects.all()


@pytest.fixture
def s3file():
    file_name = 'temp.txt'
    with open(file_name, 'w') as f:
        f.write("content")

    yield file_name

    os.remove(file_name)
