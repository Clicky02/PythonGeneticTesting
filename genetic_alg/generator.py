from itertools import product
import random
from typing import Any, Callable
from genetic_alg.candidate import Candidate
from genetic_alg.parsing.parameter import ParameterDetail
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.population import Population
from genetic_alg.types.type_info import TypeInfo
from genetic_alg.types.basic import basic_type_infos


class GeneticTestGenerator:
    """
    The main way to use our genetic testing library.
    """

    random_candidate_count: int
    interesting_chance: float
    supported_types: dict[type, TypeInfo]

    def __init__(
        self,
        random_candidate_count: int = 10,
        interesting_chance: float = 0.3,
        supported_types: list[TypeInfo] = basic_type_infos,
    ) -> None:
        self.random_candidate_count = random_candidate_count
        self.interesting_chance = interesting_chance

        self.supported_types = {}
        for val in supported_types:
            self.supported_types[val.type] = val

    def create_population_for(self, target: Callable):
        """
        Creates an initial population given a function you want to test.
        """

        fdetails = FunctionDetails.from_func(target)

        for param in fdetails.args:
            if param.type not in self.supported_types:
                raise Exception(f"Function contains unsupported type '{param.type}'")

        # for _ in range(self.population_size):
        #     candidates.append(signature.create_empty_candidate())

        interesting_vals_by_arg = [self.supported_types[param.type].interesting_values for param in fdetails.args]
        interesting_value_candidates = [Candidate(list(combo)) for combo in product(*interesting_vals_by_arg)]

        rand_candidates: list[Candidate] = [
            self.create_random_candidate(fdetails) for _ in range(self.random_candidate_count)
        ]

        return Population(target, fdetails, interesting_value_candidates + rand_candidates)

    def create_random_candidate(self, fdetails: FunctionDetails):
        """
        Randomly creates a candidate for a target function
        """
        candidate_args = []
        for param in fdetails.args:
            candidate_args.append(self.create_random_value(param))
        return Candidate(candidate_args)

    def create_random_value(self, param: ParameterDetail):
        """
        Randomly creates a value for a function parameter
        """

        type_info = self.supported_types[param.type]
        if random.random() < self.interesting_chance:
            return type_info.get_random_interesting()
        return type_info.create_random()
