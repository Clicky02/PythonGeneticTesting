import ast
from dataclasses import dataclass
from importlib import import_module
import inspect
from types import GenericAlias
from typing import Any, Callable


@dataclass
class ConstantSearchState:
    func: Callable
    identifiers: list[str]


def find_constants_rec(node: ast.AST, parents: list[ast.AST], state: ConstantSearchState):
    constants = set()

    # print(node)

    if isinstance(node, ast.Name):
        if node.id.isupper() and node.id not in state.identifiers:
            # print(f"Found Constant {node.id} ")
            mod = import_module(state.func.__module__)

            if hasattr(mod, node.id):
                constants.add(getattr(mod, node.id))

    if isinstance(node, ast.Assign):
        for child in node.targets:
            if isinstance(node, ast.Name):
                state.identifiers.append(node.id)

    if isinstance(node, ast.Constant):
        # print(f"Found Constant {node} with type={type(node.value)} and value={node.value}")
        constants.add(node.value)

    for child in ast.iter_child_nodes(node):
        constants.update(find_constants_rec(child, parents, state))

    return constants


def find_constants(func: Callable) -> dict[type | GenericAlias, list]:
    f_ast = ast.parse(inspect.getsource(func))
    constants = find_constants_rec(f_ast, [], ConstantSearchState(func, []))
    return split_and_sort_constants(constants)


def split_and_sort_constants(constants: set):
    cons_dict: dict[type | GenericAlias, list] = {}

    for constant in constants:
        if type(constant) == float or type(constant) == int:
            float_constants = cons_dict.get(float, [])
            float_constants.append(constant)
            cons_dict[float] = float_constants

            int_constants = cons_dict.get(int, [])
            int_constants.append(constant)
            cons_dict[int] = int_constants
        elif type(constant) in cons_dict:
            cons_dict[type(constant)].append(constant)
        else:
            cons_dict[type(constant)] = [constant]

    return cons_dict
