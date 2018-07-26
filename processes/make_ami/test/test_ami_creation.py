import pytest

import import_make_ami
import make_ami


@pytest.mark.ami
def test_make_blank_ami():
    image_id = make_ami.blank(
        volume_size=22
    )

    print(image_id)
    assert image_id


@pytest.mark.ami
def test_make_python3_ami():
    output = make_ami.python3(
        volume_size=22
    )

    print(output)
    assert output


@pytest.mark.skip(reason='Need to create python3 ami first')
@pytest.mark.ami
def test_make_notify_only_ami():
    output = make_ami.python3(
        volume_size=22
    )

    print(output)
    assert output
