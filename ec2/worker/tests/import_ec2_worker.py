import pathlib as pl
import sys

path = pl.Path(__file__).parent / '..' / 'src'

if str(path) not in sys.path:
    sys.path.append(str(path))
