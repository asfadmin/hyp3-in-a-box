"""
Cmd line interface for hyp3_process module

based off of: https://medium.com/@trstringer/the-easy-and-nice-way-to-do-cli-apps-in-python-5d9964dc950d
"""

import os
import sys

import boto3
import requests

from .process import Process


def main():
    add_cwd_to_path()

    try:
        import hyp3_handler
        handler_function = hyp3_handler.handler
    except ImportError:
        print('ERROR: hyp3_handler.py not found in cwd')
    except AttributeError:
        print('ERROR: no function named handler in hyp3_handler.py')
    else:
        process = Process(
            handler_function=handler_function
        )
        process.run()

    try:
        terminate()
    except Exception as e:
        print('WARNING: Unable to terminate '
              'instance (probably not running on an ec2 instance)')


def add_cwd_to_path():
    sys.path.insert(0, os.getcwd())


def terminate():
    resp = requests.get(
        "http://169.254.169.254/latest/meta-data/instance-id"
    )
    instance_id = resp.text
    boto_response = \
        boto3.client('autoscaling').terminate_instance_in_auto_scaling_group(
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=True
        )
    print(f"Terminating instance: \n{boto_response}")


if __name__ == "__main__":
    main()
