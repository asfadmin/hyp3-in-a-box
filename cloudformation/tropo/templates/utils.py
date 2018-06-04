import pathlib as pl
import json


def get_map(name):
    file_path, file_name = pl.Path(__file__).parent, name + '.json'

    map_path = file_path / 'maps' / file_name

    with map_path.open('r') as f:
        template_map = json.load(f)

    return template_map
