import time

import user_data
import ec2


def blank(volume_size):
    return create_ami(
        base_ami_id="ami-ba602bc2",
        user_data_filename="",
        ami_name='ubuntu-copy',
        volume_size=22
    )


def python3(volume_size):
    return create_ami(
        base_ami_id="ami-ba602bc2",
        user_data_filename="python3",
        ami_name='ubuntu-python3',
        volume_size=22
    )


def notify_only(volume_size):
    return create_ami(
        base_ami_id='not created yet...',
        user_data_filename='notify_only',
        ami_name='hyp3-notify-only-process',
        volume_size=22
    )


def create_ami(**kwargs):
    ami_name = kwargs['ami_name']
    images = ec2.check_for_existing_image(ami_name)

    if image_already_exists(images):
        print('image already created...', ami_name)
        return ec2.get_existing_image_from(images)
    else:
        print('creating new image', ami_name)
        return make_new_image(**kwargs)


def make_new_image(*, base_ami_id, user_data_filename, ami_name, volume_size):
    ami_user_data = user_data.load(user_data_filename)

    instance_args = {
        "ami_id": base_ami_id,
        "volume_size": volume_size,
        "user_data": ami_user_data
    }

    with ec2.instance(**instance_args) as instance:
        return make_ami(instance, ami_name)


def image_already_exists(images):
    return "Images" in images and len(images['Images']) > 0


def make_ami(instance, image_name):
    print('waiting for instance to stop after user data is finished')
    wait_for_user_data()

    print("Creating AMI from running instance")
    image = instance.create_image(
        Description='Compute environment resource for time series processing',
        Name=image_name
    )

    print(image)

    print('waiting for image to finish creating')
    while image.state == 'pending':
        time.sleep(5)
        image.load()

    if image.state == 'available':
        print("AMI created successfully")
    else:
        print("!!!!AMI creation FAILED!!!!")

    return image.id


def wait_for_user_data():
    print('View logs user data logs in instance at:'
          ' \n  /var/log/cloud-init-output.log\n')
    print(f'"{user_data.user_data_finish_file()}"',
          'will be created at the end of the user data script',
          'in the home directory.')

    while True:
        user_in = input("User data finished? (yes/no) ")
        if 'yes' in user_in:
            return
