import json

import random_password


def lambda_handler(event, context):
    print(json.dumps(event))

    random_password.send_response(event)

    return 'SUCCESS'
