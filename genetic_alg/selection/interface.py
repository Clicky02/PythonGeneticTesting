from abc import ABC, abstractmethod
import random
from genetic_alg.population import Population


class ISelection(ABC):
    """
    Interface for classes that can perform selection
    """

    @abstractmethod
    def select_on(self, population: Population) -> Population:
        """Creates a new population by selecting from the current population."""
        ...


class ElitismSelection(ISelection):
    """
    Elitism selection strategy that ensures the best candidates are carried over
    to the next generation.
    """

    def __init__(self, elite_count: int = 1, new_pop_count: int = 1):
        """
        :param elite_count: Number of top candidates to keep in the next generation.
        """
        self.elite_count = elite_count
        self.new_pop = new_pop_count

    def select_on(self, population: Population) -> Population:
        """
        Selects a new population using elitism. The top `elite_count` candidates are
        guaranteed to be carried over, while the rest are filled with randomly chosen candidates.

        :param population: The current population.
        :return: A new Population object with selected candidates.
        """
        # Sort candidates by fitness in descending order to get the best ones
        sorted_candidates = sorted(population.candidates, key=lambda candidate: candidate.fitness, reverse=True)

        # Select the elite candidates
        selected_candidates = sorted_candidates[:self.elite_count]

        # Fill the rest with the population randomly
        while len(selected_candidates) < self.new_pop:
            selected_candidates.append(random.choice(sorted_candidates))

        # Return the new population with the selected candidates
        return Population(population.target, population.target_details, selected_candidates)
