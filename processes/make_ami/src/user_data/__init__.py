import pathlib as pl


def load(name):
    if name == "":
        empty_user_data = ""

        return empty_user_data
    else:
        filename = name + '.sh'
        user_data_path = pl.Path(__file__).parent / 'user-data' / filename

        with user_data_path.open('r') as f:
            return f.read()
