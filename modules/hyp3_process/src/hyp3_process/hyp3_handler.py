from typing import Dict, NamedTuple, Callable
import functools

import asf_granule_util as gu
from hyp3_events import StartEvent

from . import working_directory
from .outputs import OutputPatterns
from . import package
from . import products


HandlerFunction = Callable[[
    gu.SentinelGranule,
    str,
    str
], Dict[str, str]
]

ProcessingFunction = Callable[[
    StartEvent,
    Dict[str, str],
    str
], Dict[str, str]
]


def make_hyp3_processing_function_from(
    handler_function: HandlerFunction
) -> ProcessingFunction:
    def hyp3_wrapper(
            job: StartEvent,
            earthdata_creds: Dict[str, str],
            products_bucket: str
    ) -> Dict[str, str]:
        granule = gu.SentinelGranule(job.granule)

        with working_directory.create(granule) as working_dir:
            download_granule(granule, earthdata_creds, working_dir)

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


def download_granule(granule, earthdata_creds, working_dir):
    print(f'downloading granule {granule}')

    gu.download(
        granule,
        earthdata_creds,
        directory=str(working_dir)
    )
