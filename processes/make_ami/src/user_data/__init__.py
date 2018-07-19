import pathlib as pl


def load(name):
    if name == "":
        user_data = ""
    else:
        filename = name + '.sh'
        user_data_path = pl.Path(__file__).parent / 'user-data' / filename

        with user_data_path.open('r') as f:
            user_data = f.read()

    return user_data + user_data_finished()


def user_data_finished():
    return "echo 'user data finished' > " + user_data_finish_file()


def user_data_finish_file():
    return "user-data-finished.txt"
