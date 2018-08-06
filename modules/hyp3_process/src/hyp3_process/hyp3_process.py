from typing import Dict, NamedTuple, Callable, Union
import functools

import asf_granule_util as gu
from hyp3_events import RTCSnapJob

from . import working_directory
from .outputs import OutputPatterns
from . import package
from . import products


class EarthdataCredentials(NamedTuple):
    username: str
    password: str


HandlerFunc = Callable[[
    RTCSnapJob,
    EarthdataCredentials,
    str
], Dict[str, str]
]


class Process:
    def __init__(
        self,
        earthdata_creds: EarthdataCredentials,
        products_bucket: str
    ) -> None:
        self.earthdata_creds = earthdata_creds
        self.products_bucket = products_bucket

        self.process_handler: Union[HandlerFunc, None] = None

    def handler(self, process_func: HandlerFunc):
        if self.process_handler is not None:
            raise HandlerRedefinitionError(
                'Process is only allowed one handler function'
            )

        self.process_handler = hyp3_handler(process_func)

    def start(self, job):
        return self.process_handler(
            job,
            self.earthdata_creds,
            self.products_bucket
        )


def hyp3_handler(handler_function) -> HandlerFunc:
    def hyp3_wrapper(
            job: RTCSnapJob,
            earthdata_creds: EarthdataCredentials,
            products_bucket: str
    ) -> Dict[str, str]:
        granule = gu.SentinelGranule(job.granule)

        with working_directory.create(granule) as working_dir:
            gu.download(granule, earthdata_creds, directory=str(working_dir))

            handler_function(granule, working_dir, job.script_path)

            patterns = OutputPatterns(**job.output_patterns)

            process_outputs = package.outputs(
                archive_name=f'{granule}-rtc-snap',
                working_dir=working_dir,
                output_patterns=patterns
            )

            product_zip_url, browse_url = products.upload(
                outputs=process_outputs,
                bucket_name=products_bucket
            )

        return {
            'product_url': product_zip_url,
            'browse_url': browse_url
        }

    return hyp3_wrapper


class HandlerRedefinitionError(Exception):
    pass
