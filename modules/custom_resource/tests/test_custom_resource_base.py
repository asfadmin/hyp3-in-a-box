import pathlib as pl
import json

import import_custom_resource
import custom_resource


def test_valid_custom_resoure_base():
    event = get_sample_event()

    resp = ValidBaseTester(event) \
        .get_response()

    assert isinstance(resp, dict)


def test_invalid_process_return_values():
    event = get_sample_event()

    for BadCls in (InvalidDictBaseTester, InvalidTypeBaseTester):
        resp = BadCls(event) \
            .get_response()

        assert resp['Status'] == 'FAILED'


class ValidBaseTester(custom_resource.Base):
    def _process(self):
        return {
            'Data': {'Value': 'base tester'},
            'Reason': 'Successfully generated a random string'
        }


class InvalidTypeBaseTester(custom_resource.Base):
    def _process(self):
        return {
            'Dat': {'Value': 'base tester'},
            'eason': 'Successfully generated a random string'
        }


class InvalidDictBaseTester(custom_resource.Base):
    def _process(self):
        return ['bad ret value']


def get_sample_event():
    path = pl.Path(__file__).parent / 'data' / 'sample_event.json'

    with path.open('r') as f:
        return json.load(f)
