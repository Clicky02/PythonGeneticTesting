from math import ceil
from typing import override
from genetic_alg.candidate import Candidate
from genetic_alg.population import Population
from genetic_alg.selection.interface import ISelection


import random


class RouletteWheelSelection(ISelection):
    """
    Roulette wheel selection strategy that selects candidates based on their relative fitness.
    Candidates with higher fitness values have a higher probability of being selected,
    akin to a weighted random choice.

    Details:
        The total fitness of the population is calculated, and for each selection, a random
        "pick" is generated within the total fitness range. Each candidate's fitness adds
        to a cumulative total, and the candidate that brings the cumulative total above
        the random "pick" threshold is selected.
    """

    # TODO: Add a without replacement option?

    @override
    def select_from(self, candidates: list[Candidate], total_fitness: float) -> Candidate:
        pick = random.uniform(0, total_fitness)

        current = 0
        for candidate in candidates:
            current += candidate.fitness
            if current >= pick:
                return candidate

        return candidates[-1]
