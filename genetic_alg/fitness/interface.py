from abc import ABC, abstractmethod

from genetic_alg.population import Population


class IFitness(ABC):
    """
    Interface for classes that can calculate fitness.
    """

    @abstractmethod
    def evaluate_on(self, population: Population): ...
