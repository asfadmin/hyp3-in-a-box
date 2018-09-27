import os
import pathlib as pl
from typing import Dict, Callable
import time

from asf_granule_util import SentinelGranule
from hyp3_events import StartEvent

from . import working_directory as wd
from .outputs import OutputPatterns
from . import package
from . import products
from ..daemon import log


HandlerFunction = Callable[[
    SentinelGranule,
    Dict[str, str]
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
    """ Convertes a **handler function -> process function**

        A handler function is a function which runs arbitrary processing
        code and is not connected to HyP3. Handler functions are responsible
        downloading their own data. This includes granules and DEM files.
        Granules can be easily downloaded using the `asf_granule_util`_ module.

        .. _asf_granule_util: http://asf-docs.s3-website-us-west-2.amazonaws.com/asf-granule-util/

        The handler function will be run in a directory with the process code
        in the current directory. Any modification to the file system should be
        made only below the current directory.

        .. code-block:: python

           def handler_function(
               granule_name: str,
               earthdata_creds: Dict[str, str]
           ):
               ...

        Processing functions wrap functionality around a handler function and
        are for interfacing with HyP3.

        .. code-block:: python

           def process_function(
               job: StartEvent,
               earthdata_creds: Dict[str, str],
               products_bucket: str
           ) -> Dict[str, str]:
               ...

        **A processing function:**

            1. Sets up a working directory
            2. Runs handler function in working directory
            3. Packages any outputs
            4. Uploads outputs to s3
            5. Return presigned urls for outputs
    """
    def hyp3_wrapper(
            job: StartEvent,
            earthdata_creds: Dict[str, str],
            products_bucket: str
    ) -> Dict[str, str]:
        start = time.time()

        granule = SentinelGranule(job.granule)
        temp_path = working_dir_path(granule)
        link_dir = pl.Path.cwd()

        with wd.create(temp_path, link_dir) as working_dir:
            os.chdir(working_dir)
            handler_function(
                str(granule),
                earthdata_creds
            )

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

        log.info(f'total processing time: {time.time() - start}')

        return {
            'product_url': product_zip_url,
            'browse_url': browse_url
        }

    return hyp3_wrapper


def working_dir_path(granule: SentinelGranule) -> pl.Path:
    return pl.Path.home() / 'jobs' / working_dir_name(granule.unique_id)


def working_dir_name(job_name: str) -> str:
    return f'GRAN-{job_name}'
