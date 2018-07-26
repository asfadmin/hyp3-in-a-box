import collections

import boto3
import mock
from hypothesis import given, strategies as st

import import_make_ami
import ec2

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')


def test_client_functions_exist():
    assert ec2_client.describe_images
    assert ec2_client.terminate_instances


def test_resource_functions_exist():
    assert ec2_resource.Image
    assert ec2_resource.create_instances


@mock.patch('ec2.ec2_client.describe_images')
@given(st.text())
def test_ec2_describe_images(ec2_mock, image_id):
    assert isinstance(image_id, str)
    ec2.get_image(image_id)

    ec2_mock.assert_called_with(ImageIds=[image_id])


@mock.patch('ec2.ec2_client.terminate_instances')
@given(st.text())
def test_ec2_terminate(ec2_mock, instance_id):
    Instance = collections.namedtuple('Instance', ['id'])
    instance = Instance(instance_id)

    ec2.terminate(instance)

    ec2_mock.assert_called_with(InstanceIds=[instance_id])
