import itertools
from genetic_alg.fitness.shared_statement import SharedStatementFitness
from genetic_alg.generator import GeneticTestGenerator
from genetic_alg.selection.roulette import RouletteWheelSelection
from genetic_alg.selection.tournament import TournamentSelection

# from genetic_alg.selection.elitism import ElitismSelection
from tests import testable_int, testable_str, testable_float


if __name__ == "__main__":

    gen = GeneticTestGenerator(
        SharedStatementFitness(),
        TournamentSelection(),
        random_candidate_count=20,
        interesting_chance=0.2,
        percent_candidates_preserved=0.5,
        elite_count=3,
    )

    print("INT TEST")
    pops = gen.run_on(testable_int, 100)

    print("\n\nFLOAT TEST")
    pops = gen.run_on(testable_float, 100)

    print("\n\nSTRING TEST")
    pops = gen.run_on(testable_str, 100)
