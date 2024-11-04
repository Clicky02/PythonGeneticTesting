import random
import string
from genetic_alg.types.type_info import TypeInfo


def random_int(*_):
    return random.randint(-1000000, 1000000)


def decrement(val):
    return val - 1


def increment(val):
    return val + 1


def negate(val):
    return val * -1


int_type_info = TypeInfo[int](int, random_int, [random_int, decrement, increment, negate], [0])


def random_float(*_):
    return random.random()


float_type_info = TypeInfo[float](float, random_float, [random_float, decrement, increment, negate], [0])


def random_bool(*_):
    return random.randint(0, 1) == 0


def flip_bool(val: bool):
    return not val


bool_type_info = TypeInfo[bool](bool, random_bool, [flip_bool], [True, False])


def random_string(*_):
    length = random.randint(1, 50)
    random_string = "".join(random.choice(string.printable) for _ in range(length))
    return random_string


def add_char(val: str):
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + random.choice(string.printable) + val[pos:]


def remove_char(val: str):
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + val[pos + 1 :]


str_type_info = TypeInfo[str](
    str,
    random_string,
    [random_string, add_char, remove_char],
    [""],
)

basic_type_infos = [int_type_info, float_type_info, bool_type_info, str_type_info]
