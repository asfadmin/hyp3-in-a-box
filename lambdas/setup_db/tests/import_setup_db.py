import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
new_path = os.path.join(path, '../src')
if new_path not in sys.path:
    sys.path.append(new_path)
