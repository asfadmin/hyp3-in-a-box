import pathlib as pl

import import_rtc_snap
import products


def test_products(tmpdir, testing_bucket):
    paths = create_fake_zip_and_browse(tmpdir)

    product_link = products.upload(
        paths=paths,
        bucket_name=testing_bucket
    )

    assert product_link


def create_fake_zip_and_browse(directory):
    working_dir = pl.Path(directory)

    paths = [working_dir / f for f in ('output.zip', 'browse.png')]

    for path in paths:
        path.parent.mkdir(exist_ok=True, parents=True)

        with path.open('w') as f:
            f.write('testing dummy file')

    return paths
