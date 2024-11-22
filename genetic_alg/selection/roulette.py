from genetic_alg.population import Population
from genetic_alg.selection.interface import ISelection


import random


class RouletteWheelSelection(ISelection):
    """
    Roulette wheel selection strategy that selects candidates based on their relative fitness.
    Candidates with higher fitness values have a higher probability of being selected,
    akin to a weighted random choice.

    Methods:
        select_on(population: Population) -> Population:
            Runs the selection process using a probability distribution based on
            candidate fitness and returns a new population of selected candidates.

    Details:
        The total fitness of the population is calculated, and for each selection, a random
        "pick" is generated within the total fitness range. Each candidate's fitness adds
        to a cumulative total, and the candidate that brings the cumulative total above
        the random "pick" threshold is selected.
    """

    def select_on(self, population: Population) -> Population:
        total_fitness = sum(candidate.fitness for candidate in population.candidates)
        selected_candidates = []

        for _ in range(len(population.candidates)):
            pick = random.uniform(0, total_fitness)
            current = 0
            for candidate in population.candidates:
                current += candidate.fitness
                if current >= pick:
                    selected_candidates.append(candidate)
                    break

        return Population(population.target, population.target_details, selected_candidates)
