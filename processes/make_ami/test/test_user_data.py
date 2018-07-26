import pathlib as pl

from hypothesis import given, strategies as st

import import_make_ami
import user_data


def user_data_files():
    user_data_path = pl.Path(__file__).parent / '../src/user_data/user-data'

    return [
        str(f.name[:-3]) for f in user_data_path.iterdir()
        if str(f).endswith('sh')
    ]


@given(st.sampled_from(user_data_files()))
def test_load_user_data(name):
    ami_user_data = user_data.load(name)

    assert isinstance(ami_user_data, str)

    assert any(
        ami_user_data.startswith(shebang)
        for shebang in ('#!/bin/bash', '#! /bin/bash')
    )

    assert ami_user_data.endswith(
        user_data.self_termination_script()
    )

    print(ami_user_data)


def test_load_user_data_with_empty_name():
    assert user_data.load("") == user_data.self_termination_script()
