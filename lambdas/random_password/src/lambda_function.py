import random
import string
import uuid
import httplib
import urlparse
import json


def lambda_handler(event, context):
    print(json.dumps(event))
    response = CustomResource(event).get_response()

    return send_response(event, response)


class CustomResource:
    def __init__(self, event):
        self.event = event

    def get_response(self):
        resource_id = self.event.get(
            'PhysicalResourceId',
            str(uuid.uuid4())
        )

        response = {
            'StackId': self.event['StackId'],
            'RequestId': self.event['RequestId'],
            'LogicalResourceId': self.event['LogicalResourceId'],
            'Status': 'SUCCESS',

            'PhysicalResourceId': resource_id
        }

        if self.event['RequestType'] == 'Delete':
            return response

        try:
            process_output = self.process()
        except CustomResourceException as e:
            response.update({
                'Status': 'FAILED',
                'Reason': str(e)
            })

        response.update(process_output)

        return response

    def process(self):
        random_string = self.get_random_string()

        return {
            'Data': {'RandomString': random_string},
            'Reason': 'Successfully generated a random string'
        }

    def get_random_string(self):
        try:
            length = int(self.event['ResourceProperties']['Length'])
        except KeyError:
            raise CustomResourceException('Must specify a length')
        except ValueError:
            raise CustomResourceException('Length not an integer')

        characters = string.digits + string.ascii_letters

        random_string = ''.join(
            random.SystemRandom().choice(characters) for _ in range(length)
        )

        return random_string


class CustomResourceException(Exception):
    pass


def send_response(request, response):
    if not ('ResponseURL' in request or request['ResponseURL']):
        return response

    url = urlparse.urlparse(request['ResponseURL'])
    body = json.dumps(response)
    https = httplib.HTTPSConnection(url.hostname)
    https.request('PUT', url.path+'?'+url.query, body)

    return response
