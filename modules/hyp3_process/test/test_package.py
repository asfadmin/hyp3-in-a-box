import pathlib as pl
import zipfile as zf

import pytest

import rtc_snap_strategies as strats
import import_hyp3_process
from hyp3_process.handler import package
from hyp3_process.handler.outputs import OutputPatterns


valid_cases = [({
    'input_files': ['granule/hello.txt', 'test2.txt', 'test.png'],
    'patterns': OutputPatterns(archive=['*/*.txt'], browse=['*.png']),
    'expected': [['granule/hello.txt'], 'test.png']
}), ({
    'input_files': strats.rtc_example_files(),
    'patterns': OutputPatterns(
        archive=["*/*_TC_G??.tif", "*/*.txt", "*/*.png"],
        browse=['*/*GVV.png']
    ),
    'expected': strats.rtc_output()
})]

error_cases = [({
    'input_files': ['hello.txt', 'test.png'],
    'patterns': OutputPatterns(archive=['*/*.txt'], browse=['*.png']),
    'expected': package.NoFilesFoundForOutputPattern
}), ({
    'input_files': ['dir/hello.txt'],
    'patterns': OutputPatterns(archive=['*/*.txt'], browse=['*.png']),
    'expected': package.NoBrowseFound
})]


@pytest.mark.parametrize("case", valid_cases)
def test_valid_package_outputs(make_working_dir, case):
    working_dir = make_working_dir(case['input_files'])
    archive_name = 'name-for-outputs'

    output_archive, browse = package.outputs(
        archive_name=archive_name,
        working_dir=working_dir,
        output_patterns=case['patterns']
    )

    assert output_archive.suffix == '.zip'
    assert archive_name in output_archive.name
    assert zf.is_zipfile(output_archive)

    expected_archive, expected_browse = case['expected']

    with zf.ZipFile(output_archive, 'r') as z:
        assert set(z.namelist()) == set(expected_archive)

    assert browse.suffix == '.png'
    assert browse.name == pl.Path(expected_browse).name


@pytest.mark.parametrize("case", error_cases)
def test_package_invalid_cases(make_working_dir, case):
    working_dir = make_working_dir(case['input_files'])
    archive_name = 'name-for-outputs'

    with pytest.raises(case['expected']):
        output_archive, browse = package.outputs(
            archive_name=archive_name,
            working_dir=working_dir,
            output_patterns=case['patterns']
        )
