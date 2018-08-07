import pytest
import mock

import import_hyp3_process
from hyp3_process import Process, HandlerRedefinitionError


def fake_arguments():
    return {
        'queue_name': 'hyp3-in-a-box-test-Hyp3StartEvents-UH7H3GF3M057.fifo',
        'sns_arn': 'arn:aws:sns:us-west-2:765666652335:'
        'hyp3-in-a-box-test-Hyp3FinishEventSNSTopic-13WBNBJMEKOMK',
        'earthdata_creds': '{"username": "dummy", "password": "banana"}',
        'products_bucket': 'hyp3-in-a-box-products',
        'are_ssm_param_names': False
    }


@pytest.mark.skip
@mock.patch(
    'hyp3_process.hyp3_process.get_arguments',
    side_effect=fake_arguments
)
def test_process_run_full(args_mock, event_in_queue, process):
    process.run()


def test_process_run_fails_with_no_arguments(process):
    with pytest.raises(SystemExit):
        process.run()


def test_process_can_only_have_one_handler(process):
    with pytest.raises(HandlerRedefinitionError):
        def second_handler():
            pass

        process.add_handler(second_handler)


@pytest.fixture
def process():
    proc = Process()

    proc.add_handler(lambda *args, **kwargs: 'hello!')

    return proc
