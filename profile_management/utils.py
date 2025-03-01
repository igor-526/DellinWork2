import random
import string


def get_random_password(length):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for _ in range(length))