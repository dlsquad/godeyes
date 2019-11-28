import base64
import random


def gen_code():
    return "".join(str(i) for i in random.choices(range(0, 9), k=6))
