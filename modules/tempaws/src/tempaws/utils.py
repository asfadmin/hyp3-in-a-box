import random
import string

def unique_id(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
