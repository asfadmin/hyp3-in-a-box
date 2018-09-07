import pytest

import import_custom_metric
from target_calculation import calculate_metric


# messages / instance = 10

def test_custom_metric_calculation(expected):
    print("\nmessages: " + str([v[1] for v in expected]))

    for current_instances in range(10):
        print("\n" + str(current_instances) + ": ", end="")

        for i, m in expected:
            metric = calculate_metric(
                num_messages=m, num_instances=current_instances
            )

            print(metric, end=", ")


@pytest.fixture
def expected():
    return [
        (0, 0),
        (1, 5),
        (1, 10),
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
