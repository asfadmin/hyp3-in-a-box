import os


def get_environ_params(*args):
    return [
        os.environ[k] for k in args
    ]
