import pathlib as pl
import zipfile as zf
import pytest

import rtc_snap_strategies as strats

import import_rtc_snap
import package

package_test_cases = [(
    ['granule/hello.txt', 'test2.txt', 'test.png'],
    ['*/*.txt', '*.png'],
    ['granule/hello.txt', 'test.png']
), (
    ['hello.txt', 'test.png'],
    ['*/*.txt'],
    []
), (
    strats.rtc_example_files(),
    ["*/*_TC_G??.tif", "*/*.png", "*/*.txt"],
    strats.rtc_example_files()
)]


@pytest.mark.parametrize(
    "file_paths,patterns,expected",
    package_test_cases
)
def test_package(tmpdir, file_paths, patterns, expected):
    working_dir = tmpdir.mkdir('product-outputs')
    create_output_files(
        file_paths,
        working_dir
    )

    output_zip = package.outputs_from(
        'output.zip',
        str(working_dir),
        patterns
    )

    assert output_zip.endswith('.zip')
    assert zf.is_zipfile(output_zip)

    with zf.ZipFile(output_zip, 'r') as z:
        assert set(z.namelist()) == set(expected)


def create_output_files(output_paths, working_dir):
    for p in output_paths:
        full_path = pl.Path(working_dir) / p

        write_sample_file(full_path)


def write_sample_file(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as f:
        f.write('test')


@pytest.fixture()
def output_patterns():
    return
