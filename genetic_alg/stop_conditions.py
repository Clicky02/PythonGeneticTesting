from genetic_alg.population import Population


def perfect_coverage(_generations: int, population: Population):
    return population.coverage >= 0.99999


def max_generations(max_generation: int):
    def stop_when(generations: int, population: Population):
        return population.coverage >= 0.99999 or generations >= max_generation

    return stop_when
