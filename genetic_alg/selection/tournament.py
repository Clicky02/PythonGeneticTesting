from genetic_alg.population import Population
from genetic_alg.selection.interface import ISelection


import random


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
