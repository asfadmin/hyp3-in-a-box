import random
import string
import uuid
import httplib
import urlparse
import json

"""
If included in a Cloudformation build as a CustomResource, generate a random
string of length given by the 'length' parameter.
By default the character set used is upper and lowercase ascii letters plus
digits.  If the 'punctuation' parameter is specified this also includes
punctuation. If you specify a KMS key ID then it will be encrypted, too.
"""


def lambda_handler(event, context):
    response = {
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Status': 'SUCCESS'
    }

    if 'PhysicalResourceId' in event:
        response['PhysicalResourceId'] = event['PhysicalResourceId']
    else:
        response['PhysicalResourceId'] = str(uuid.uuid4())

    if event['RequestType'] == 'Delete':
        return send_response(event, response)

    try:
        length = int(event['ResourceProperties']['Length'])
    except KeyError:
        return send_response(
            event,
            response,
            status='FAILED',
            reason='Must specify a length'
        )
    except ValueError:
        return send_response(
            event,
            response,
            status='FAILED',
            reason='Length not an integer'
        )

    try:
        rds_compatible = event['ResourceProperties']['RDSCompatible']
    except KeyError:
        rds_compatible = False

    valid_characters = string.ascii_letters+string.digits

    if rds_compatible not in [False, 'false', 'False']:
        valid_characters = valid_characters.translate(None, '@/"')

    random_string = ''.join(random.SystemRandom().choice(
        string.digits + string.ascii_letters) for _ in range(length))

    response['Data'] = {
        'RandomString': random_string
    }
    response['Reason'] = 'Successfully generated a random string'

    return send_response(event, response)


def send_response(request, response, status=None, reason=None):
    if status is not None:
        response['Status'] = status

    if reason is not None:
        response['Reason'] = reason

    if 'ResponseURL' in request and request['ResponseURL']:
        url = urlparse.urlparse(request['ResponseURL'])
        body = json.dumps(response)
        https = httplib.HTTPSConnection(url.hostname)
        https.request('PUT', url.path+'?'+url.query, body)

    return response
