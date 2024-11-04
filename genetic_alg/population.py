from dataclasses import dataclass
from typing import Any, Callable

from genetic_alg.candidate import Candidate
from genetic_alg.parsing.function import FunctionDetails


@dataclass
class Population:
    """
    Contains all candidates for genetic testing and the function the population is targeting.
    """

    target: Callable
    target_details: FunctionDetails
    candidates: list[Candidate]
    total_fitness: float = 0
