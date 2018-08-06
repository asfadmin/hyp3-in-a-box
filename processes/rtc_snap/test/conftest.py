import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--full-rtc-snap", action="store_true",
        default=False, help="Full rtc-snap-runthrough"
    )
    parser.addoption(
        "--fake-rtc-snap", action="store_true",
        default=False, help="Fake rtc-snap-runthrough"
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--fake-rtc-snap"):
        skip_funcs_with_flag('fake_rtc_snap', items)
    if not config.getoption("--full-rtc-snap"):
        skip_funcs_with_flag('full_rtc_snap', items)


def skip_funcs_with_flag(flag, items):
    skip_rtc_runthrough = pytest.mark.skip(
        reason=f"need {flag} option to run"
    )

    for item in items:
        if flag in item.keywords:
            item.add_marker(skip_rtc_runthrough)
