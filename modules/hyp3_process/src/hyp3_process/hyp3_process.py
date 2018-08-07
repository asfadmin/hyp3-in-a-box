from typing import Union
import argparse


from .hyp3_handler import (
    hyp3_handler,
    HandlerFunction,
    ProcessingFunction
)

from .hyp3_daemon import HyP3DaemonConfig, HyP3Daemon


class Process:
    def __init__(self) -> None:
        self.process_handler: Union[ProcessingFunction, None] = None

    def handler(self, process_func: HandlerFunction):
        if self.process_handler is not None:
            raise HandlerRedefinitionError(
                'Process is only allowed one handler function'
            )

        self.process_handler = hyp3_handler(process_func)

    def start(self, job):
        return self.process_handler(
            job, {}, ''
        )

    def run(self):
        args = get_arguments()

        config = HyP3DaemonConfig(**args)

        process_daemon = HyP3Daemon(
            config,
            self.process_handler
        )

        process_daemon.run()


def get_arguments():
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
            description=f'SSM Param name for {ssm_arg}'
        )

    return cli


class HandlerRedefinitionError(Exception):
    pass
