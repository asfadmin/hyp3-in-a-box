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


class Process:
    """
    Wraps process HyP3 processing functionality around a lambda function
    """

    def __init__(self, *, handler_function: HandlerFunction) -> None:
        """ Turn handler function into processing function"""
        self.process_handler: ProcessingFunction = \
            make_hyp3_processing_function_from(handler_function)

    def run(self) -> None:
        """ Run process in background as daemon process """
        assert self.process_handler is not None

        args = get_arguments()
        log.debug('HyP3 Daemon Args: \n%s', json.dumps(args))

        creds = json.loads(args['earthdata_creds'])
        bucket, queue_name, sns_arn = [
            args[k] for k in ["product_bucket", "queue_name", "sns_arn"]
        ]

        worker = HyP3Worker(self.process_handler, creds, bucket)

        email_topic = sns.Topic(sns_arn)
        job_queue = sqs.get_queue_by_name(
            QueueName=queue_name
        )

        process_daemon = HyP3Daemon(
            job_queue,
            email_topic,
            worker
        )

        process_daemon.run()

    def start(
        self,
        job: StartEvent,
        earthdata_creds: Dict[str, str],
        product_bucket: str
    ) -> Dict[str, str]:
        """ Start a single job for processing"""

        assert self.process_handler is not None

        return self.process_handler(
            job, earthdata_creds, product_bucket
        )


def get_arguments():
    """ Get arguments for HyP3DaemonConfig"""

    if 'STACK_NAME' in os.environ:
        log.info('args from environment')
        args = get_arguments_from_environment()
    else:
        log.info('args from cli')
        args = get_arguments_with_cli()
        log.info(args)

    return args


def get_arguments_from_environment():
    stack = os.environ['STACK_NAME']

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


def get_arguments_with_cli():
    cli = parser()
    return vars(cli.parse_args())


def parser():
    cli = argparse.ArgumentParser(description='Cli for hyp3 process')

    ssm_args = [
        'queue_name',
        'sns_arn',
        'earthdata_creds',
        'products_bucket',
    ]

    for ssm_arg in ssm_args:
        cli.add_argument(
            f'--{ssm_arg}', type=str, required=True,
            dest=ssm_arg, help=f'SSM Param name for {ssm_arg}'
        )

    return cli
