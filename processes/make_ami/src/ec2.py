import contextlib

import boto3


ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')


@contextlib.contextmanager
def instance(**kwargs):
    try:
        print('creating instance')
        instance = create(
            **kwargs
        ).pop()

        print('waiting for instance to start...')
        wait_until_running(instance)

        yield instance
    finally:
        print("Terminating instance '{}'".format(instance.id))
        terminate(instance)


def create(*, ami_id, volume_size, user_data, keypair_name='asf-wbhorn'):
    return ec2_resource.create_instances(
        BlockDeviceMappings=[{
            'DeviceName': '/dev/xvdcz',
            'VirtualName': 'ephemeral0',
            'Ebs': {
                'Encrypted': False,
                'DeleteOnTermination': True,
                'VolumeSize': int(volume_size),
                'VolumeType': 'gp2'
            }
        }],
        ImageId=ami_id,
        InstanceType='t2.micro',
        KeyName=keypair_name,
        UserData=user_data,
        MaxCount=1, MinCount=1,
        Monitoring={'Enabled': False},
        TagSpecifications=get_tags()
    )


def get_image(image_id):
    return ec2_client.describe_images(ImageIds=[image_id])[0]


def check_for_existing_image(ami_name):
    return ec2_client.describe_images(
        Filters=[{
            'Name': 'name',
            'Values': [ami_name]
        }]
    )


def get_existing_image_from(images):
    return ec2_resource.Image(images['Images'][0]['ImageId'])


def get_tags():
    return [
        get_tag(resource_type) for resource_type in ('instance', 'volume')
    ]


def get_tag(resource_type):
    return {
        'ResourceType': resource_type,
        'Tags': [{
            'Key': 'Name',
            'Value': 'ComputeEnvironmentAMI'
        }]
    }


def wait_until_running(instance):
    print("Instance '{}' created... "
          "Waiting for instance to start".format(instance.id)
          )

    instance.wait_until_running()
    instance.load()


def terminate(instance):
    ec2_client.terminate_instances(
        InstanceIds=[
            instance.id
        ]
    )
