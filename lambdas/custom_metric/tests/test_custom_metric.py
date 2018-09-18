import pytest

import import_custom_metric
from target_calculation import calculate_metric


def test_possible_combos(expected):
    print("\nmessages: " + str([v[1] for v in expected]))

    for current_instances in range(10):
        print("\n" + str(current_instances) + ": ", end="")

        for i, m in expected:
            metric = calculate_metric(
                num_messages=m, num_instances=current_instances
            )

            print(metric, end=", ")


def test_startup_messages_make_instance():
    for m in range(1, 10):
        metric = calculate_metric(
            num_messages=m, num_instances=0
        )

        assert metric == 2


def test_no_messages_no_instances():
    for i in range(10):
        metric = calculate_metric(
            num_messages=0, num_instances=i
        )

        assert metric == 0


@pytest.fixture
def expected():
    return [
        (0, 0),
        (2, 5),
        (2, 10),
        (2, 15),
        (2, 20),
        (3, 30),
        (4, 40),
        (5, 50),
        (6, 60),
        (7, 70),
        (8, 80),
        (9, 90)
    ]
