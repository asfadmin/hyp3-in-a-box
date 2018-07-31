import asf_granule_util as gu
import pytest
import mock

import import_rtc_snap
import working_directory


@mock.patch('working_directory._teardown')
@mock.patch('working_directory._make')
def test_working_directory(make_mock, teardown_mock, granule):
    with working_directory.create(granule) as wd:
        assert granule.unique_id in wd
        assert 'job' in wd

    make_mock.assert_called_once()
    teardown_mock.assert_called_once()


@pytest.fixture()
def granule():
    return gu.SentinelGranule(
        'S1A_WV_SLC__1SSV_20180728T102445_20180728T102956_022993_027EDC_40F7'
    )