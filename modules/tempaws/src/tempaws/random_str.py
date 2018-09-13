import random
import string


def make(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
