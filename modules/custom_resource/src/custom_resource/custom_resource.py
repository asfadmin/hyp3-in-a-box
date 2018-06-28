import abc
import http.client
from urllib.parse import urlparse
import uuid
import json


class Base(abc.ABC):
    def __init__(self, event):
        self.event = event

    @abc.abstractmethod
    def _process(self):
        """ Run the process for the custom resource

            :rtype: dict
            :returns:

            .. code-block:: python

               {'Data': {...}, 'Reason': 'reason str here'}
        """
        return NotImplemented

    def get_response(self):
        response = self._get_response_defaults()

        if self.event['RequestType'] == 'Delete':
            return response

        try:
            process_output = self._process()
            validate_process_ouptut(process_output)
        except CustomResourceException as e:
            response.update({
                'Status': 'FAILED',
                'Reason': str(e)
            })
        else:
            response.update(process_output)

        return response

    def _get_response_defaults(self):
        resource_id = self.event.get(
            'PhysicalResourceId',
            str(uuid.uuid4())
        )

        return {
            'StackId': self.event['StackId'],
            'RequestId': self.event['RequestId'],
            'LogicalResourceId': self.event['LogicalResourceId'],
            'Status': 'SUCCESS',

            'PhysicalResourceId': resource_id
        }


def validate_process_ouptut(output):
    check_output_type(output)
    check_values_in(output)


def check_output_type(output):
    if not isinstance(output, dict):
        err_msg = (
            'ERROR: value returned from CustomResource._process '
            "must be of type 'dict'."
        )

        raise CustomResourceException(err_msg)


def check_values_in(output):
    try:
        assert 'Data' in output
        assert 'Reason' in output

        assert isinstance(output['Data'], dict)
        assert isinstance(output['Reason'], str)
    except AssertionError:
        err_msg = 'Malformed dict returned from CustomResource._process'

        raise CustomResourceException(err_msg)


def send(request, response):
    if 'ResponseURL' not in request:
        return response

    url = urlparse(request['ResponseURL'])
    response_json = json.dumps(response)

    connection = http.client.HTTPSConnection(url.hostname)

    connection.request(
        'PUT', f'{url.path}?{url.query}',
        response_json
    )

    return response


class CustomResourceException(Exception):
    pass
