from genetic_alg.candidate import Candidate
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

    Details:
        For each selection, a subset of `tournament_size` candidates is chosen at random
        from the population. The candidate with the highest fitness in this subset wins
        the tournament and is added to the next generation.
    """

    def __init__(self, tournament_size: int = 3):
        self.tournament_size = tournament_size

    def select_from(self, candidates: list[Candidate], total_fitness: float) -> Candidate:
        tournament = random.sample(candidates, self.tournament_size)
        return max(tournament, key=lambda candidate: candidate.fitness)
