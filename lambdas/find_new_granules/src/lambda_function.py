import os

import find_new
from find_new import environment as env
import results


def lambda_handler(event, context):
    env_setup()

    search_results = find_new.granules()

    return results.package(search_results)


def env_setup():
    env.set_is_production(True)

    bucket = os.environ['PREVIOUS_TIME_BUCKET']
    env.set_bucket(bucket)
