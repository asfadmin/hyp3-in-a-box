import pathlib as pl
from typing import NamedTuple, List


class OutputPatterns(NamedTuple):
    archive: List[str]
    browse: str


class ProcessOutputs(NamedTuple):
    archive: pl.Path
    browse: pl.Path
