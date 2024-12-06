from copy import copy, deepcopy
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


def decrement(val, *_):
    return val - 1


def increment(val, *_):
    return val + 1


def negate(val, *_):
    return val * -1


int_type_info = TypeInfo[int](int, random_int, [decrement, increment, negate], [0])


def random_float(*_):
    return random.random() * 200000 - 100000


float_type_info = TypeInfo[float](float, random_float, [decrement, increment, negate], [0])


def random_bool(*_):
    return random.randint(0, 1) == 0


def flip_bool(val: bool, *_):
    return not val


bool_type_info = TypeInfo[bool](bool, random_bool, [flip_bool], [True, False])


def random_string(*_):
    length = random.randint(1, 25)
    random_string = "".join(random.choice(string.printable) for _ in range(length))
    return random_string


def add_char(val: str, *_):
    # If the string is empty, add a single character to start with
    if not val:
        return random.choice(string.printable)

    # For non-empty strings, add a character at a random position
    pos = random.randint(0, len(val))
    return val[:pos] + random.choice(string.printable) + val[pos:]


def add_str(val: str, self_type: TypeInfo[str], ctx: GeneticContext):
    # If the string is empty, just create a new string
    if not val:
        return self_type.random(ctx)

    # For non-empty strings, add a character at a random position
    pos = random.randint(0, len(val))
    return val[:pos] + self_type.random(ctx) + val[pos:]


def remove_char(val: str, *_):
    # If the string is empty, return it as is (nothing to remove)
    if not val:
        return val

    # For non-empty strings, remove a character at a random position
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + val[pos + 1 :]


def remove_str(val: str, self_type: TypeInfo[str], ctx: GeneticContext):
    pos = random.randint(0, len(val))
    length = len(self_type.random(ctx))
    return val[:pos] + val[pos + length :]


def change_char(val: str, *_):
    # If the string is empty, return it as is (nothing to remove)
    if not val:
        return val

    # For non-empty strings, remove a character at a random position
    pos = random.randint(0, len(val) - 1)
    return val[:pos] + random.choice(string.printable) + val[pos + 1 :]


str_type_info = TypeInfo[str](str, random_string, [change_char, add_char, remove_char, add_str, remove_str], [""])


# Define values for a new generic type `list`.
def random_list(self_type: TypeInfo, types: list[TypeInfo], ctx: GeneticContext):
    (inner_type,) = types
    return [inner_type.random(ctx) for _ in range(random.randint(1, 10))]


def add_element(val: list, self_type: TypeInfo, generic_types: list[TypeInfo], ctx: GeneticContext):
    (inner_type,) = generic_types
    val = deepcopy(val)
    val.append(inner_type.random(ctx))
    return val


def remove_element(val: list, *_):
    val = deepcopy(val)
    if val:
        val.pop(random.randint(0, len(val) - 1))
    return val


def mutate_element(val: list, self_type: TypeInfo, types: list[TypeInfo], ctx: GeneticContext):
    (inner_type,) = types
    val = deepcopy(val)
    if len(val) > 0:
        i = random.randint(0, len(val) - 1)
        val[i] = inner_type.mutate(val[i], ctx)
    return val


list_type_info = GenericTypeInfo[list](list, 1, random_list, [add_element, remove_element, mutate_element], [[]])


# Define values for a new generic type `list`.
def random_dict(self_type: TypeInfo, types: list[TypeInfo], ctx: GeneticContext):
    (key_type, value_type) = types
    return {key_type.random(ctx): value_type.random(ctx) for _ in range(1, 10)}


def add_entry(val: dict, self_type: TypeInfo, generic_types: list[TypeInfo], ctx: GeneticContext):
    (key_type, value_type) = generic_types
    val = deepcopy(val)
    val[key_type.random(ctx)] = value_type.random(ctx)
    return val


def remove_entry(val: dict, *_):
    val = deepcopy(val)
    if len(val) > 0:
        val.pop(random.choice(list(val.keys())))
    return val


def mutate_key(val: dict, self_type: TypeInfo, generic_types: list[TypeInfo], ctx: GeneticContext):
    (key_type, value_type) = generic_types
    val = deepcopy(val)
    if len(val) > 0:
        old_key = random.choice(list(val.keys()))
        new_key = key_type.mutate(old_key, ctx)
        val[new_key] = val.pop(old_key)
    return val


def mutate_value(val: dict, self_type: TypeInfo, generic_types: list[TypeInfo], ctx: GeneticContext):
    (key_type, value_type) = generic_types
    val = deepcopy(val)
    if len(val) > 0:
        key = random.choice(list(val.keys()))
        val[key] = value_type.mutate(val[key], ctx)
    return val


dict_type_info = GenericTypeInfo[dict](dict, 2, random_dict, [add_entry, remove_entry, mutate_key, mutate_value], [{}])


# Define values for a new type `tuple[int]`.
def random_int_tuple(*_):
    return (random.randint(-100, 100), random.randint(-100, 100))


def reverse_tuple(val: tuple, *_):
    return val[::-1]


tuple_type_info = TypeInfo[tuple](tuple, random_int_tuple, [reverse_tuple], [(0, 0)])


# Define values for a new type `set[int]`.
def random_int_set(*_):
    return {random.randint(-100, 100) for _ in range(random.randint(1, 10))}


def add_to_set(val: set[int], *_):
    val.add(random.randint(-100, 100))
    return val


def remove_from_set(val: set[int], *_):
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

basic_generic_type_infos_list = [list_type_info, dict_type_info]

default_registry = TypeRegistry(basic_type_infos_list, basic_generic_type_infos_list)
