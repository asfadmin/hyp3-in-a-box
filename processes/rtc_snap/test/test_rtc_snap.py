import pathlib as pl
import json

import pytest

import hyp3_events

import import_rtc_snap
import hyp3_handler


@pytest.mark.full_rtc_snap
def test_rtc_snap_full_run(tmpdir, rtc_snap_job, earthdata_creds):
    print('running rtc_snap with processing')
    hyp3_handler.handler(
        'S1A_IW_GRDH_1SDV_20180801T155817_20180801T155842_023055_0280C4_749A',
        str(tmpdir),
        earthdata_creds,
        ('/home/ubuntu/hyp3-in-a-box/processes/rtc_snap/build'
        '/hyp3-rtc-snap/src/procSentinelRTC-3.py')
    )


def resp_is_correct(resp):
    return all([
        isinstance(resp, dict),
        'product_url' in resp,
        'browse_url' in resp
    ])


@pytest.fixture()
def earthdata_creds():
    try:
        path = pl.Path(__file__).parent / 'earthdata-creds.json'

        with path.open('r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'username': 'test', 'password': 'creds'}


@pytest.fixture()
def rtc_snap_job():
    return hyp3_events.StartEvent(
        granule=('S1A_IW_GRDH_1SDV_20180801T155817'
                 '_20180801T155842_023055_0280C4_749A'),
        user_id=1,
        sub_id=1,
        output_patterns={
            'archive': ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
            'browse': '*/*GVV.png'
        },
        additional_info=[],
        script_path=str(
            pl.Path(__file__).parent /
            './../build/hyp3-rtc-snap/src/procSentinelRTC-3.py'
        )
    )
