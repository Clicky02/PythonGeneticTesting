from __future__ import annotations
from dataclasses import dataclass
import random
from types import GenericAlias
from typing import Any
from genetic_alg.types.basic import TypeDict
from genetic_alg.types.type_info import TypeInfo
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.parsing.parameter import ParamKind, ParameterDetail


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
        return [self.arg_values[i] for i in range(len(self.arg_values)) if func.args[i].kind != ParamKind.KEYWORD_ONLY]

    def kwargs(self, func: FunctionDetails) -> dict[str, Any]:
        return {
            func.args[i].name: self.arg_values[i]
            for i in range(len(self.arg_values))
            if func.args[i].kind == ParamKind.KEYWORD_ONLY
        }
    
    def to_str(self, func: FunctionDetails, type_dict: TypeDict) -> str:
        def format_arg(val: Any, arg_info: ParameterDetail):
            return type_dict[arg_info.type].to_str(val)
        
        def format_kwarg(val: Any, arg_info: ParameterDetail):
            return f"{arg_info.name}={type_dict[arg_info.type].to_str(val)}"
        
        arg_strs = ([
                format_arg(self.arg_values[i], func.args[i])
                for i in range(len(self.arg_values)) 
                if func.args[i].kind != ParamKind.KEYWORD_ONLY
            ] + [
                format_kwarg(self.arg_values[i], func.args[i])
                for i in range(len(self.arg_values)) 
                if func.args[i].kind == ParamKind.KEYWORD_ONLY
            ]
        )

        return f"{func.name}({", ".join(arg_strs)})"

