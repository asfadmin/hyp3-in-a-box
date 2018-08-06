import pathlib as pl

import pytest

import import_add_subs
import subscription

FILE_PATH = pl.Path(__file__).parent


@pytest.mark.skip
@pytest.mark.skipif(
    not (FILE_PATH / '../src/cfg/cfg.json').exists(),
    reason="Can't run test without cfg"
)
def test_make_subscriptions():
    resps = subscription.make(
        subs_file_path=str(
            FILE_PATH / 'data/subs.json'
        )
    )

    assert isinstance(resps, list)
