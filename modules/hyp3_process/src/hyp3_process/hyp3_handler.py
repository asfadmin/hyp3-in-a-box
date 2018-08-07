from typing import Dict, NamedTuple, Callable
import functools

import asf_granule_util as gu
from hyp3_events import StartEvent

from . import working_directory
from .outputs import OutputPatterns
from . import package
from . import products


class EarthdataCredentials(NamedTuple):
    username: str
    password: str


HandlerFunction = Callable[[
    gu.SentinelGranule,
    str,
    str
], Dict[str, str]
]

ProcessingFunction = Callable[[
    StartEvent,
    EarthdataCredentials,
    str
], Dict[str, str]
]


def hyp3_handler(handler_function: HandlerFunction) -> ProcessingFunction:
    def hyp3_wrapper(
            job: StartEvent,
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
