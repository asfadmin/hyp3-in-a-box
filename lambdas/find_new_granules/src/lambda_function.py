from . import find_new as fn


def lambda_handler(event, context):
    granules = fn.get_new()

    print(granules)
