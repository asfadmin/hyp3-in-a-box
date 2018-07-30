
CACHE = {}


def with_name(key):
    def cache_value(function):
        def wrapper(*args, **kwargs):
            if key not in CACHE:
                CACHE[key] = function(*args, **kwargs)

            return CACHE[key]
        return wrapper
    return cache_value
