from typing import Dict
import json
import os
import argparse

from hyp3_events import StartEvent

from .handler import (
    make_hyp3_processing_function_from,
    HandlerFunction,
    ProcessingFunction
)

from .hyp3_daemon import HyP3DaemonConfig, HyP3Daemon, log


class Process:
    def __init__(self, *, handler_function) -> None:
        self.add_handler(handler_function)

    def run(self) -> None:
        args = get_arguments()
        log.debug('Hyp3 Daemon Args: \n%s', json.dumps(args))

        config = HyP3DaemonConfig(**args)

        assert self.process_handler is not None

        process_daemon = HyP3Daemon(
            config,
            self.process_handler
        )

        process_daemon.run()

    def add_handler(self, handler_function: HandlerFunction) -> None:
        self.process_handler: ProcessingFunction = \
            make_hyp3_processing_function_from(
                handler_function
            )

    def start(
        self,
            job: StartEvent,
            earthdata_creds: Dict[str, str],
            product_bucket: str
    ) -> Dict[str, str]:
        assert self.process_handler is not None

        return self.process_handler(
            job, earthdata_creds, product_bucket
        )


def get_arguments():
    if 'STACK_NAME' in os.environ:
        log.info('args from environment')
        args = get_arguments_from_environment()
    else:
        log.info('args from cli')
        args = get_arguments_with_cli()
        args['are_ssm_param_names'] = False
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
        param: f"/{stack}/{param_name}" for (param, param_name) in params
    }


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
