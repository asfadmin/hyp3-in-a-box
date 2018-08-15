import pathlib as pl

import import_hyp3_process
from hyp3_process.handler.outputs import OutputPatterns, ProcessOutputs


def test_output_pattern_class():
    assert OutputPatterns(
        archive=['*/*.txt'],
        browse='*.png',
    )


def test_process_outputs_class():
    assert ProcessOutputs(
        archive=[pl.Path('granule/hello.txt')],
        browse=pl.Path('test.png')
    )
