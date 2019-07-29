import argparse
import contextlib
from datetime import datetime
import pathlib as pl
import sys
import json
from typing import Dict
import os

import boto3

from hyp3_events import StartEvent

from .handler import (
    make_hyp3_processing_function_from,
    HandlerFunction
)

from .daemon import HyP3Daemon, HyP3Worker, log

ssm = boto3.client('ssm')
sns = boto3.resource('sns')
sqs = boto3.resource('sqs')
s3_client = boto3.client('s3')


SSM_PARAMS = [
    'StartEventQueueName',
    'FinishEventSNSArn',
    'EarthdataCredentials',
    'ProductsS3Bucket'
]


def make_daemon_with(handler_function: HandlerFunction) -> HyP3Daemon:
    """ Configure and run in background as daemon process"""

    args = get_arguments()
    log.debug('HyP3 Daemon Args: \n%s', json.dumps(args))

    queue, topic_arn, creds_json, bucket = [
        args[k] for k in SSM_PARAMS
    ]

    job_queue = sqs.get_queue_by_name(QueueName=queue)
    email_topic = sns.Topic(topic_arn)

    logger = Logger(bucket=bucket)

    process_handler = make_hyp3_processing_function_from(handler_function)
    creds = json.loads(creds_json)

    worker = HyP3Worker(process_handler, creds, bucket)

    return HyP3Daemon(
        job_queue,
        email_topic,
        logger,
        worker
    )


def get_arguments():
    stack = get_cli_args()['stack_name']

    process_args = get_arguments_for(stack)
    log.info(process_args)

    return process_args


def get_cli_args():
    cli = parser()

    return vars(cli.parse_args())


def parser():
    cli = argparse.ArgumentParser(description='Cli for hyp3 process')

    cli.add_argument(
        f'--stack-name', dest='stack_name', type=str,
        required=True, help='Stack name to run off of'
    )

    return cli


def get_arguments_for(stack: str) -> Dict[str, str]:
    return {
        param: load_param(f"/{stack}/{param}")
        for param in SSM_PARAMS
    }


def load_param(param):
    val = ssm.get_parameter(
        Name=param,
        WithDecryption=True
    )['Parameter']['Value']

    log.debug(f"{param} -> {val}")

    return val


class Logger:
    def __init__(self, name, bucket):
        self.bucket = bucket

    @contextlib.contextmanager
    def stdout_to_file(self, name):
        old_stdout = sys.stdout
        log = pl.Path.home() / 'log'

        if not log.exists():
            log.mkdir(parents=True)

        log_file = log / name

        with log_file.open('w') as log:
            sys.stdout = log
            yield
            sys.stdout = old_stdout

        bucket_path = str(pl.Path('log') / self.name)

        s3_client.upload_file(str(log_file), self.bucket, bucket_path)
