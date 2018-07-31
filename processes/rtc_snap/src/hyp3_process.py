import asf_granule_util as gu

import working_directory
import rtc_snap
import package
import products


def hyp3_handler(rtc_snap_job):
    granule = gu.SentinelGranule(rtc_snap_job.granule)

    with working_directory.create(granule) as working_dir:
        gu.download(granule, directory=str(working_dir))

        rtc_snap.process(granule, working_dir)

        output_zip = package.outputs_from(
            zip_name='output.zip',
            working_dir=working_dir,
            file_patterns=rtc_snap_job.output_file_patterns
        )

        product_urls = products.upload(
            paths=[output_zip_path],
            bucket_name=get_bucket_name()
        )

    return {
        'product_url': product_urls[0]
    }


def get_bucket_name():
    return 'hyp3-in-a-box-products'
