from copy import copy
import random
import string
from types import GenericAlias
from typing import TypeAlias
from genetic_alg.context import GeneticContext
from genetic_alg.types.registry import TypeRegistry
from genetic_alg.types.type_info import GenericTypeInfo, TypeInfo

"""
This file contains the TypeInfo definitions for all the basic types that we support.
"""


def random_int(*_):
    return random.randint(-100000, 100000)


def decrement(val, ctx: GeneticContext):
    return val - 1


def increment(val, ctx: GeneticContext):
    return val + 1


def negate(val, ctx: GeneticContext):
    return val * -1


int_type_info = TypeInfo[int](int, random_int, [decrement, increment, negate], [0])


def random_float(*_):
    return random.random() * 200000 - 100000


float_type_info = TypeInfo[float](float, random_float, [decrement, increment, negate], [0])


def random_bool(*_):
    return random.randint(0, 1) == 0


def flip_bool(val: bool, ctx: GeneticContext):
    return not val


bool_type_info = TypeInfo[bool](bool, random_bool, [flip_bool], [True, False])


def random_string(*_):
    length = random.randint(1, 25)
    random_string = "".join(random.choice(string.printable) for _ in range(length))
    return random_string


def add_char(val: str, ctx: GeneticContext):
    # If the string is empty, add a single character to start with
    if not val:
        return random.choice(string.printable)

    # For non-empty strings, add a character at a random position
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + random.choice(string.printable) + val[pos:]


def remove_char(val: str, ctx: GeneticContext):
    # If the string is empty, return it as is (nothing to remove)
    if not val:
        return val

    # For non-empty strings, remove a character at a random position
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + val[pos + 1 :]


def change_char(val: str, ctx: GeneticContext):
    # If the string is empty, return it as is (nothing to remove)
    if not val:
        return val

    # For non-empty strings, remove a character at a random position
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + random.choice(string.printable) + val[pos + 1 :]


str_type_info = TypeInfo[str](str, random_string, [change_char, add_char, remove_char], [""])


# Define values for a new generic type `list`.
def random_list(types: list[TypeInfo], ctx: GeneticContext):
    (inner_type,) = types
    return [inner_type.random(ctx) for _ in range(random.randint(1, 10))]


def add_element(val: list, types: list[TypeInfo], ctx: GeneticContext):
    (inner_type,) = types
    val = copy(val)
    val.append(inner_type.random(ctx))
    return val


def remove_element(val: list, _types: list[TypeInfo], ctx: GeneticContext):
    val = copy(val)
    if val:
        val.pop(random.randint(0, len(val) - 1))
    return val


def mutate_element(val: list, types: list[TypeInfo], ctx: GeneticContext):
    (inner_type,) = types
    val = copy(val)
    if len(val) > 0:
        i = random.randint(0, len(val) - 1)
        val[i] = inner_type.mutate(val[i], ctx)
    return val


list_type_info = GenericTypeInfo[list](list, 1, random_list, [add_element, remove_element, mutate_element], [[]])


# Define values for a new type `dict[int]`.
def random_dict(*_):
    return {random.choice(string.ascii_lowercase): random.randint(-100, 100) for _ in range(random.randint(1, 5))}


def add_key_value(val: dict, ctx: GeneticContext):
    val[random.choice(string.ascii_lowercase)] = random.randint(-100, 100)
    return val


def remove_key(val: dict, ctx: GeneticContext):
    if val:
        val.pop(random.choice(list(val.keys())))
    return val


dict_type_info = TypeInfo[dict[str, int]](dict[str, int], random_dict, [add_key_value, remove_key], [{}])


# Define values for a new type `tuple[int]`.
def random_int_tuple(*_):
    return (random.randint(-100, 100), random.randint(-100, 100))


def reverse_tuple(val: tuple, ctx: GeneticContext):
    return val[::-1]


tuple_type_info = TypeInfo[tuple](tuple, random_int_tuple, [reverse_tuple], [(0, 0)])


# Define values for a new type `set[int]`.
def random_int_set(*_):
    return {random.randint(-100, 100) for _ in range(random.randint(1, 10))}


def add_to_set(val: set[int], ctx: GeneticContext):
    val.add(random.randint(-100, 100))
    return val


def remove_from_set(val: set[int], ctx: GeneticContext):
    if val:
        val.pop()
    return val


set_type_info = TypeInfo[set[int]](set[int], random_int_set, [add_to_set, remove_from_set], [set()])

basic_type_infos_list = [
    int_type_info,
    float_type_info,
    bool_type_info,
    str_type_info,
    dict_type_info,
    set_type_info,
    tuple_type_info,
]

basic_generic_type_infos_list = [list_type_info]

default_registry = TypeRegistry(basic_type_infos_list, basic_generic_type_infos_list)
