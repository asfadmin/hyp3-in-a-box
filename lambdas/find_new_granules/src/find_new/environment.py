
IS_PRODUCTION = True


def set_is_production(val):
    global IS_PRODUCTION

    if not isinstance(val, bool):
        raise Exception('is_production can only be a boolean value')

    IS_PRODUCTION = val
