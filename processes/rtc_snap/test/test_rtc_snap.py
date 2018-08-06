import pathlib as pl
import json

import pytest

import hyp3_events

import import_rtc_snap
from rtc_snap import rtc_snap


@pytest.mark.fake_rtc_snap
def test_rtc_snap_with_fake(
    rtc_snap_fake_job,
    earthdata_creds
):
    rtc_snap.earthdata_creds = earthdata_creds,
    rtc_snap.products_bucket = 'hyp3-in-a-box-products'

    resp = rtc_snap.start(rtc_snap_fake_job)

    assert resp_is_correct(resp)


@pytest.mark.full_rtc_snap
def test_rtc_snap_full_run(rtc_snap_full_job, earthdata_creds):
    print('running rtc_snap with processing')
    resp = rtc_snap.process(
        rtc_snap_full_job,
        earthdata_creds,
        'hyp3-in-a-box-products'
    )

    assert resp_is_correct(resp)


def resp_is_correct(resp):
    return all([
        isinstance(resp, dict),
        'product_url' in resp,
        'browse_url' in resp
    ])


@pytest.fixture()
def rtc_snap_fake_job():
    return rtc_job_with_script_path(
        str(
            pl.Path(__file__).parent / './fak'
        )
    )


@pytest.fixture()
def rtc_snap_full_job():
    return rtc_job_with_script_path(
        str(
            pl.Path(__file__).parent /
            './../build/hyp3-rtc-snap/src/procSentinelRTC-3.py'
        )
    )


@pytest.fixture()
def earthdata_creds():
    path = pl.Path(__file__).parent / 'earthdata-creds.json'

    with path.open('r') as f:
        return json.load(f)


@pytest.fixture()
def rtc_snap_fake_script():
    return rtc_job_with_script_path(
        str(pl.Path(__file__).parent / 'fake-rtc-script.py')
    )


def rtc_job_with_script_path(path):
    return hyp3_events.RTCSnapJob(
        granule=('S1A_IW_GRDH_1SDV_20180801T155817'
                 '_20180801T155842_023055_0280C4_749A'),
        address='test@email.com',
        username='test-user',
        subscription='test-subscription',
        output_patterns={
            'archive': ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
            'browse': '*/*GVV.png'
        },
        script_path=path
    )
