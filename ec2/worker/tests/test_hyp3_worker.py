import contextlib
import pathlib as pl
import os

import mock

import import_hyp3_worker
import hyp3_worker


@mock.patch('hyp3_worker.start_worker')
def test_hyp3_worker(worker_start_mock):
    hyp3_worker.run()
    worker_start_mock.assert_called_once()
