import pathlib as pl

import pytest

import import_add_subs
import subscription


@pytest.mark.skipif(
    not (pl.Path(__file__).parent / '../src/cfg/cfg.json').exists(),
    reason="Can't run test without cfg"
)
def test_make_subscriptions():
    resps = subscription.make()

    assert isinstance(resps, list)
