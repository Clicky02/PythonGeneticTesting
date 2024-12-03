from dataclasses import dataclass
import inspect
from typing import Callable, Self

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

        *_, last_line_info = func.__code__.co_lines()
        last_line = last_line_info[2]

        if last_line is None:
            raise Exception("Something went wrong.")

        return cls(args, func.__name__, func_file, first_line, last_line)
