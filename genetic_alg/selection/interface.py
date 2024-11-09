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


class TournamentSelection(ISelection):
    """
    Tournament selection strategy that selects candidates by running a mini "tournament"
    among randomly chosen candidates. The candidate with the highest fitness in each
    tournament is selected for the next generation.

    Attributes:
        tournament_size (int): The number of candidates participating in each tournament.

    Methods:
        select_on(population: Population) -> Population:
            Runs a selection process by choosing candidates through a tournament
            mechanism and returns a new population of selected candidates.

    Details:
        For each selection, a subset of `tournament_size` candidates is chosen at random
        from the population. The candidate with the highest fitness in this subset wins
        the tournament and is added to the next generation.
    """

    def __init__(self, tournament_size: int = 3):
        self.tournament_size = tournament_size

    def select_on(self, population: Population) -> Population:
        selected_candidates = []

        for _ in range(len(population.candidates)):
            tournament = random.sample(population.candidates, self.tournament_size)
            winner = max(tournament, key=lambda candidate: candidate.fitness)
            selected_candidates.append(winner)

        return Population(population.target, population.target_details, selected_candidates)


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
