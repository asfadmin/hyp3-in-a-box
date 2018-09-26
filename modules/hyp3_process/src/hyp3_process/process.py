from typing import Dict
import json
import os
import argparse

import boto3

from hyp3_events import StartEvent

from .handler import (
    make_hyp3_processing_function_from,
    HandlerFunction,
    ProcessingFunction
)

from .daemon import HyP3Daemon, HyP3Worker, log

ssm = boto3.client('ssm')
sns = boto3.resource('sns')
sqs = boto3.resource('sqs')


def run(handler_function) -> None:
    """ Run process in background as daemon process """

    args = get_arguments()
    log.debug('HyP3 Daemon Args: \n%s', json.dumps(args))

    job_queue = sqs.get_queue_by_name(QueueName=args['queue_name'])

    email_topic = sns.Topic(args['sns_arn'])

    process_handler = make_hyp3_processing_function_from(handler_function)
    creds = json.loads(args['earthdata_creds'])
    worker = HyP3Worker(process_handler, creds, args['product_bucket'])

    process_daemon = HyP3Daemon(
        job_queue,
        email_topic,
        worker
    )

    process_daemon.run()


def get_arguments():
    """ Get arguments for HyP3DaemonConfig"""

    stack = get_cli_args()['stack_name']

    process_args = get_arguments_for(stack)
    log.info(process_args)

    return process_args


def get_arguments_for(stack: str) -> Dict[str, str]:
    params = [
        ('queue_name', 'StartEventQueueName'),
        ('sns_arn', 'FinishEventSNSArn'),
        ('earthdata_creds', 'EarthdataCredentials'),
        ('products_bucket', 'ProductsS3Bucket')
    ]

    return {
        param: load_param(f"/{stack}/{param_name}")
        for param, param_name in params
    }


def load_param(param):
    val = ssm.get_parameter(
        Name=param,
        WithDecryption=True
    )['Parameter']['Value']

    log.debug(f"{param} -> {val}")

    return val


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
