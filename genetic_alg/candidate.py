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

    def mutate(self, supported_types: dict[type, TypeInfo], mutation_rate: float = 0.1):
        """
        Randomly mutates one or more values in arg_values based on the mutation rate,
        using the mutation functions specified in the TypeInfo instances.

        :param supported_types: A dictionary mapping types to TypeInfo instances.
        :param mutation_rate: The probability of mutating each argument.
        """
        for i in range(len(self.arg_values)):
            if random.random() < mutation_rate:
                value = self.arg_values[i]
                value_type = type(value)

                # Get the TypeInfo for the value's type
                if value_type in supported_types:
                    type_info = supported_types[value_type]
                    # Choose a mutation function at random
                    mutation_function = random.choice(type_info.mutators)
                    # Apply the mutation function to the value
                    mutated_value = mutation_function(value)
                    self.arg_values[i] = mutated_value
                else:
                    # Handle unsupported types if necessary
                    print(f"No TypeInfo available for type {value_type}, skipping mutation.")
        return self

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
