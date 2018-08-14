import pathlib as pl

import pytest
import mock

import import_hyp3_process
from hyp3_process.outputs import ProcessOutputs
from hyp3_process import products


@mock.patch('hyp3_process.products.products.get_bucket')
def test_products(bucket_mock, process_outputs):
    testing_bucket = 'test-bucket'
    product_url, browse_url = products.upload(
        outputs=process_outputs,
        bucket_name=testing_bucket
    )

    put_object_method = bucket_mock.return_value.put_object
    assert put_object_method.call_count == 2

    assert all(
        url for url in (product_url, browse_url)
    )

    assert product_url
    assert browse_url


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
