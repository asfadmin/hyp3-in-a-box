import sys
import pathlib as pl

path = pl.Path(__file__).parent / '..'
if path not in sys.path:
    sys.path.append(path)
