import pathlib as pl
import sys

new_path = str(pl.Path(__file__).parent / '../src')
if new_path not in sys.path:
    sys.path.append(new_path)
