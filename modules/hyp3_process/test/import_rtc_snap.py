import pathlib as pl
import sys

"""
This file adds the src directory to the import path of testing files.
"""

path = pl.Path(__file__).parent / '..' / 'src'

if str(path) not in sys.path:
    sys.path.append(str(path))
