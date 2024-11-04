from abc import ABC, abstractmethod

from genetic_alg.population import Population


class ISelection(ABC):
    """
    Interface for classes that can perform selection
    """

    @abstractmethod
    def select_on(self, population: Population) -> Population:
        """Creates a new population by selecting from the current population."""
        ...
