import pathlib as pl

import pytest

import import_rtc_snap
from outputs import ProcessOutputs
import products


def test_products(process_outputs, testing_bucket):
    product_link = products.upload(
        outputs=process_outputs,
        bucket_name=testing_bucket
    )

    assert product_link


@pytest.fixture()
def process_outputs(tmpdir):
    working_dir = pl.Path(tmpdir)

    paths = [working_dir / f for f in ('output.zip', 'browse.png')]

    for path in paths:
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open('w') as f:
            f.write('testing dummy file')

    archive, browse = paths

    return ProcessOutputs(archive, browse)
