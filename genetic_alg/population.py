from dataclasses import dataclass
from typing import Any, Callable

from genetic_alg.candidate import Candidate
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.types.basic import TypeDict


@dataclass
class Population:
    """
    Contains all candidates for genetic testing and the function the population is targeting.
    """

    target: Callable
    target_details: FunctionDetails
    candidates: list[Candidate]
    types: TypeDict
    total_fitness: float = 0
    coverage: float = 0

    def print_all_candidates(self):
        for c in self.candidates:
            print(c.to_str(self.target_details, self.types))

    def minimize(self):
        """
        Removes unnecessary candidates from the population. This will shrink the population size, 
        but maintain the same coverage. It will not necessarily find the minimal population.

        The population must have been evaluated. Otherwise, this function will raise an exception.
        """
        lines_executed = set[int]()

        sorted_candidates = sorted(self.candidates, key=lambda c: -len(c.lines_executed or []))

        new_candidates = []
        for c in sorted_candidates:
            if c.lines_executed is None:
                raise Exception("A candidate has not been evaluated.")
            
            if not c.lines_executed.issubset(lines_executed):
                lines_executed.update(c.lines_executed)
                new_candidates.append(c)

        self.candidates = new_candidates
