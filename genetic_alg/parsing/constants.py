import ast
from dataclasses import dataclass


"""
THIS FILE IS NOT USED YET
"""


@dataclass
class ConstantSearchState:
    identifiers: list[str]


def find_constants_rec(node: ast.AST, parents: list[ast.AST], state: ConstantSearchState):
    constants = []

    # print(node)

    if isinstance(node, ast.Name):
        if node.id.isupper() and node.id not in state.identifiers:
            print(f"Found Constant {node.id} ")
            # value = globals()[node.id]
            # node.

    if isinstance(node, ast.Assign):
        for child in node.targets:
            if isinstance(node, ast.Name):
                state.identifiers.append(node.id)

    if isinstance(node, ast.Constant):
        print(f"Found Constant {node} with type={type(node.value)} and value={node.value}")
        constants.append(node.value)

    for child in ast.iter_child_nodes(node):
        constants.extend(find_constants_rec(child, parents, state))

    return constants


def find_constants(node: ast.AST):
    return find_constants_rec(node, [], ConstantSearchState([]))


def split_and_sort_constants(constants: list):
    cons_dict: dict[type, list] = {}

    for constant in constants:
        if type(constant) in cons_dict:
            cons_dict[type(constant)].append(constant)
        else:
            cons_dict[type(constant)] = [constant]

    return cons_dict
