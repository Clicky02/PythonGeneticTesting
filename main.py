import itertools
from genetic_alg.fitness.shared_statement import SharedStatementFitness
from genetic_alg.generator import GeneticTestGenerator
from genetic_alg.population import Population
from genetic_alg.selection.roulette import RouletteWheelSelection
from genetic_alg.selection.tournament import TournamentSelection

# from genetic_alg.selection.elitism import ElitismSelection
from genetic_alg.stop_conditions import max_generations
from tests import longest_consecutive_subsequence, testable_int, testable_str, testable_float


if __name__ == "__main__":

    gen = GeneticTestGenerator(
        SharedStatementFitness(),
        TournamentSelection(),
        random_candidate_count=20,
        interesting_chance=0.2,
        percent_candidates_preserved=0.5,
        elite_count=3,
    )

    print("RUNNING SUBSEQUENCE TEST")
    result = gen.run_until(longest_consecutive_subsequence, max_generations(100), False)
    pop = result.population
    print(f"Result (generations={result.generations}, coverage={pop.coverage * 100}%)")
    pop.minimize()
    pop.print_all_candidates()
    print()

    print("RUNNING INT TEST")
    result = gen.run_until(testable_int, max_generations(100), False)
    pop = result.population
    print(f"Result (generations={result.generations}, coverage={pop.coverage * 100}%)")
    pop.minimize()
    pop.print_all_candidates()
    print()


    print("RUNNING FLOAT TEST")
    result = gen.run_until(testable_float, max_generations(100), False)
    pop = result.population
    print(f"Result (generations={result.generations}, coverage={pop.coverage * 100}%)")
    pop.minimize()
    pop.print_all_candidates()
    print()


    print("RUNNING STRING TEST")
    result = gen.run_until(testable_str, max_generations(100), False)
    pop = result.population
    print(f"Result (generations={result.generations}, coverage={pop.coverage * 100}%)")
    pop.minimize()
    pop.print_all_candidates()
    print()

