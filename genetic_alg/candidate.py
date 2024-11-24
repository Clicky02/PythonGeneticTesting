from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Any
from genetic_alg.types.type_info import TypeInfo
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.parsing.parameter import ParamKind


@dataclass
class Candidate:
    """
    One potential test case.
    """

    arg_values: list[Any]
    fitness: float = 0

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
        return [self.arg_values[i] for i in range(len(self.arg_values)) if func.args[i].kind != ParamKind.KEYWORD_ONLY]

    def kwargs(self, func: FunctionDetails) -> dict[str, Any]:
        return {
            func.args[i].name: self.arg_values[i]
            for i in range(len(self.arg_values))
            if func.args[i].kind == ParamKind.KEYWORD_ONLY
        }
