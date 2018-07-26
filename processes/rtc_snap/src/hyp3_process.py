import asf_granule_util as gu

import working_directory
import rtc_snap
import package
import products


def hyp3_handler(rtc_snap_job):
    granule = gu.SentinelGranule(rtc_snap_job.granule)

    working_dir = working_directory.setup(granule)

    gu.download(granule, directory=str(working_dir))

    rtc_snap.process(granule)

    output_zip = package.outputs_from(
        working_dir,
        rtc_snap_job.output_file_patterns
    )

    product_link = products.upload(output_zip, granule)

    return {
        'product_link': product_link
    }
