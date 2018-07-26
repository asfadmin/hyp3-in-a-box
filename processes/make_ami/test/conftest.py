import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--make-ami", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--make-ami"):
        return

    skip_ami = pytest.mark.skip(reason="need --make-ami option to run")
    for item in items:
        if "ami" in item.keywords:
            item.add_marker(skip_ami)
