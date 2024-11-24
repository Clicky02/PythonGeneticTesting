from abc import ABC, abstractmethod
from genetic_alg.candidate import Candidate
from genetic_alg.population import Population


class ISelection(ABC):
    """
    Interface for classes that can perform selection
    """

    @abstractmethod
    def select_from(self, candidates: list[Candidate], total_fitness: float) -> Candidate:
        """Selects a single candidate from a list of possible candidates"""
        ...
