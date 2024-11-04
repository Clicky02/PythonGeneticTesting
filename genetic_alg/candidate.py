from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Any

from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.parsing.parameter import ParamKind


@dataclass
class Candidate:
    """
    One potential test case.
    """

    arg_values: list[Any]
    fitness: float = 0

    def crossover(self, other: Candidate) -> Candidate:
        arg_count = len(self.arg_values)
        assert arg_count == len(other.arg_values)
        choose = lambda i: self.arg_values[i] if bool(random.getrandbits(1)) else other.arg_values[i]
        new_args = [choose(i) for i in range(arg_count)]
        return Candidate(new_args)

    def copy(self) -> Candidate:
        return Candidate(self.arg_values.copy())

    def args(self, func: FunctionDetails) -> list[Any]:
        return [self.arg_values[i] for i in range(len(self.arg_values)) if func.args[i].kind != ParamKind.KEYWORD_ONLY]

    def kwargs(self, func: FunctionDetails) -> dict[str, Any]:
        return {
            func.args[i].name: self.arg_values[i]
            for i in range(len(self.arg_values))
            if func.args[i].kind == ParamKind.KEYWORD_ONLY
        }
