from dataclasses import dataclass
import inspect
from typing import Callable, Self

import coverage

from genetic_alg.parsing.parameter import ParamKind, ParameterDetail


@dataclass
class FunctionDetails:
    """
    Contains useful information about a function that is necessary for testing.
    """

    args: list[ParameterDetail]

    name: str
    file: str
    first_line: int
    last_line: int
    executable_lines: set[int]

    @classmethod
    def from_func(cls, func: Callable) -> Self:
        signature = inspect.signature(func)
        parameters = signature.parameters

        args = []
        for _, param in parameters.items():
            param = ParameterDetail.from_inspect(param)

            if (
                param.kind == ParamKind.POSITIONAL_ONLY
                or param.kind == ParamKind.POSITIONAL_OR_KEYWORD
                or param.kind == ParamKind.KEYWORD_ONLY
            ):
                args.append(param)
            else:
                raise ValueError("Variable args are not supported.")

        func_file = func.__code__.co_filename
        func_file = func_file[0].upper() + func_file[1:]

        first_line = func.__code__.co_firstlineno

        last_line = first_line
        for l in func.__code__.co_lines():
            if l[2] is not None and l[2] > last_line:
                last_line = l[2]

        if last_line is None:
            raise Exception("Something went wrong.")

        cov = coverage.Coverage()
        _, executable_lines, *_ = cov.analysis2(func_file)
        executable_lines = set([l for l in executable_lines if l > first_line and l <= last_line])

        return cls(args, func.__name__, func_file, first_line, last_line, executable_lines)
