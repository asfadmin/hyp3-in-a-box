import pytest
import asf_granule_util as gu

import import_hyp3_process
import hyp3_process


def test_handler(handler, rtc_snap_job, creds, bucket):
    proc_func = hyp3_process.handler \
        .make_hyp3_processing_function_from(
            handler
        )

    result = proc_func(rtc_snap_job, creds, bucket)

    print(result)
