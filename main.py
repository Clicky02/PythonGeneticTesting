import itertools
from genetic_alg.fitness.shared_statement import SharedStatementFitness
from genetic_alg.generator import GeneticTestGenerator
from genetic_alg.population import Population
from genetic_alg.selection.roulette import RouletteWheelSelection
from genetic_alg.selection.tournament import TournamentSelection

# from genetic_alg.selection.elitism import ElitismSelection
from genetic_alg.stop_conditions import max_generations
from tests import test_funcs


if __name__ == "__main__":

    gen = GeneticTestGenerator(
        SharedStatementFitness(),
        RouletteWheelSelection(),
        pop_size=32,
        interesting_chance=0.2,
        percent_candidates_preserved=0.5,
        mutation_rate=0.1,
    )

    for func in test_funcs:
        print(f"Testing {func.__name__}...")
        result = gen.run_until(func, max_generations(250))
        result.population.minimize()
        result.population.print_all_candidates()
        print()
