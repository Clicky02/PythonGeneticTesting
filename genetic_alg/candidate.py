from __future__ import annotations
from copy import copy
from dataclasses import dataclass
import random
from types import GenericAlias
from typing import Any
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.parsing.parameter import ParamKind, ParameterDetail
from genetic_alg.types.registry import TypeRegistry


@dataclass
class Candidate:
    """
    One potential test case.
    """

    arg_values: list[Any]
    fitness: float = 0
    lines_executed: set[int] | None = None

    def crossover(self, other: Candidate) -> tuple[Candidate, Candidate]:
        arg_count = len(self.arg_values)
        assert arg_count == len(other.arg_values)

        values = [bool(random.getrandbits(1)) for _ in range(arg_count)]
        child1_args = [self.arg_values[i] if values[i] else other.arg_values[i] for i in range(arg_count)]
        child2_args = [self.arg_values[i] if not values[i] else other.arg_values[i] for i in range(arg_count)]

        return Candidate(child1_args), Candidate(child2_args)

    def copy(self) -> Candidate:
        return Candidate(self.arg_values.copy())

    def args(self, func: FunctionDetails) -> list[Any]:
        return [
            copy(self.arg_values[i]) for i in range(len(self.arg_values)) if func.args[i].kind != ParamKind.KEYWORD_ONLY
        ]

    def kwargs(self, func: FunctionDetails) -> dict[str, Any]:
        return {
            func.args[i].name: copy(self.arg_values[i])
            for i in range(len(self.arg_values))
            if func.args[i].kind == ParamKind.KEYWORD_ONLY
        }

    def to_str(self, func: FunctionDetails) -> str:
        def format_arg(val: Any):
            return repr(val)

        def format_kwarg(val: Any, arg_info: ParameterDetail):
            return f"{arg_info.name}={repr(val)}"

        arg_strs = [
            format_arg(self.arg_values[i])
            for i in range(len(self.arg_values))
            if func.args[i].kind != ParamKind.KEYWORD_ONLY
        ] + [
            format_kwarg(self.arg_values[i], func.args[i])
            for i in range(len(self.arg_values))
            if func.args[i].kind == ParamKind.KEYWORD_ONLY
        ]

        return f"{func.name}({", ".join(arg_strs)})"
