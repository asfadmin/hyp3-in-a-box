import asf_granule_util as gu

import working_directory
import rtc_snap
import package
import products


def hyp3_handler(rtc_snap_job):
    granule = gu.SentinelGranule(rtc_snap_job.granule)

    with working_directory.create(granule) as working_dir:
        gu.download(granule, directory=str(working_dir))

        rtc_snap.process(granule)

        output_zip = package.outputs_from(
            zip_name='output.zip',
            working_dir=working_dir,
            file_patterns=rtc_snap_job.output_file_patterns
        )

        product_link = products.upload(output_zip, granule)

    return {
        'product_link': product_link
    }
