import time
from genetic_alg.population import Population


def perfect_coverage(_generations: int, population: Population, start_time: float):
    return population.coverage >= 0.99999


def max_generations(max_generation: int):
    def stop_when(generations: int, population: Population, start_time: float):
        return population.coverage >= 0.99999 or generations >= max_generation

    return stop_when


def max_exec_time(max_time: float):
    """Stop condition for a maximum execution time. max_time in seconds"""

    def stop_when(generations: int, population: Population, start_time: float):
        return population.coverage >= 0.99999 or time.time() - start_time >= max_time

    return stop_when
