import ast
import inspect

from genetic_alg.parsing.constants import find_constants
from tests import testable_float, testable_str


if __name__ == "__main__":
    constants = find_constants(testable_str)
    print(constants)
