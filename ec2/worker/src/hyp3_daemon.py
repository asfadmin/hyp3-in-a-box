#!/usr/bin/env python3.6
"""
Entry point for :ref:`hyp3_process`. This file is called from ``hyp3.service``
systemd startup script
"""
import boto3
import requests

import hyp3_handler
from hyp3_process import Process


def main():
    """ Run a new process with the handler function imported from
    ``hyp3_handler.py``.
    """
    process = Process(
        handler_function=hyp3_handler.handler
    )
    process.run()

    terminate()


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


if __name__ == '__main__':
    main()
