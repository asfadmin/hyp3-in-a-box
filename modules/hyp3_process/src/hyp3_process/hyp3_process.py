from typing import Dict
import functools

import asf_granule_util as gu
from hyp3_events import RTCSnapJob

from . import working_directory
from .outputs import OutputPatterns
from . import package
from . import products


def hyp3_handler(process_func):
    def wrapper(
            job: RTCSnapJob,
            earthdata_creds: Dict[str, str]
    ) -> Dict[str, str]:
        granule = gu.SentinelGranule(job.granule)

        with working_directory.create(granule) as working_dir:
            gu.download(granule, earthdata_creds, directory=str(working_dir))

            process_func(granule, working_dir, job.script_path)

            patterns = OutputPatterns(**job.output_patterns)

            process_outputs = package.outputs(
                archive_name=f'{granule}-rtc-snap',
                working_dir=working_dir,
                output_patterns=patterns
            )

            product_zip_url, browse_url = products.upload(
                outputs=process_outputs,
                bucket_name=get_bucket_name()
            )

        return {
            'product_url': product_zip_url,
            'browse_url': browse_url
        }

    return wrapper


def get_bucket_name() -> str:
    return 'hyp3-in-a-box-products'
