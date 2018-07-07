import os

PRINT_OPTIONS = {
    'padding': 0
}


def get_environ_params(*args):
    return [
        os.environ[k] for k in args
    ]


def step_print(s):
    padding = ' ' * PRINT_OPTIONS['padding']
    print(f'{padding} - {s}')


def set_print_padding(n):
    PRINT_OPTIONS['padding'] = n
