from . import find_new as fn


def lambda_handler(event, context):
    fn.get_new()
