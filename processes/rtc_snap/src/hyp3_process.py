import asf_granule_util as gu

import working_directory
import rtc_snap
from outputs import OutputPatterns
import package
import products


def hyp3_handler(rtc_snap_job):
    granule = gu.SentinelGranule(rtc_snap_job.granule)

    with working_directory.create(granule) as working_dir:
        gu.download(granule, directory=str(working_dir))

        rtc_snap.process(granule, working_dir)

        patterns = OutputPatterns(**rtc_snap_job.output_patterns)

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


def get_bucket_name():
    return 'hyp3-in-a-box-products'
