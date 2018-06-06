import find_new
from find_new import environment as env


def lambda_handler(event, context):
    env.set_is_production(True)

    return find_new.granules()

