import pathlib as pl

import pytest

import import_rtc_snap
from outputs import ProcessOutputs
import products


def test_products(process_outputs, testing_bucket):
    product_url, browse_url = products.upload(
        outputs=process_outputs,
        bucket_name=testing_bucket
    )

    assert all(
        s3_key_has_no_folder(url, testing_bucket)
        for url in (product_url, browse_url)
    )

    assert product_url
    assert browse_url


def s3_key_has_no_folder(url, bucket_name):
    path_start = url.find(bucket_name) + len(bucket_name)

    return pl.Path(url[path_start:]).parent == pl.Path('/')


@pytest.fixture()
def process_outputs(tmpdir):
    working_dir = pl.Path(tmpdir)

    paths = [working_dir / f for f in ('output.zip', 'test/browse.png')]

    for path in paths:
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open('w') as f:
            f.write('testing dummy file')

    archive, browse = paths

    return ProcessOutputs(archive, browse)
