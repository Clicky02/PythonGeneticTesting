import itertools
from genetic_alg import population
from genetic_alg.fitness.shared_statement_fitness import SharedStatementFitness
from genetic_alg.generator import GeneticTestGenerator
from genetic_alg.selection.interface import ElitismSelection, TournamentSelection, RouletteWheelSelection
from genetic_alg.population import Population
from tests import testable_int, testable_str, testable_float


def preform_genetic_testing(p, types):
    SharedStatementFitness().evaluate_on(p)

    print(f"INITIAL POPULATION: {p}"
          f"\n"
          f"INITIAL POPULATION SIZE: {len(p.candidates)}"
          f"\n")

    # Initialize the Selection Strategy
    elite_count = 2
    # initialize how many candidates from the population you want
    new_population_count = elite_count

    elite_strategy = ElitismSelection(elite_count, new_population_count)
    tournament_strategy = TournamentSelection()
    random_strategy = RouletteWheelSelection()

    # Run selection to create a new population
    for strategy in [elite_strategy, tournament_strategy, random_strategy]:
        print(f"CURRENT STRATEGY: {strategy}")
        new_population = strategy.select_on(p)
        print(f"NEW POPULATION: {new_population}"
              f"\n"
              f"NEW POPULATION SIZE: {len(new_population.candidates)}"
              f"\n")

        new_pop_candidates = [i for i in new_population.candidates]

        # preform all combinations of crossovers
        crossover_population = new_pop_candidates
        for combination in itertools.combinations(new_pop_candidates, 2):
            parent1, parent2 = combination[0], combination[1]
            print(f"PARENT 1: {parent1}"
                  "\n"
                  f"PARENT 2: {parent2}")
            cross1 = parent1.crossover(parent2)
            cross2 = parent2.crossover(parent1)
            print(f"CROSSOVER 1: {parent1.crossover(parent2)}")
            print(f"CROSSOVER 2: {parent2.crossover(parent1)}\n")
            crossover_population.append(cross1)
            crossover_population.append(cross2)

        print(f"\nCANDIDATES AFTER CROSSOVER: {crossover_population}")

        # Apply mutation to each candidate in the crossover population
        for candidate in crossover_population:
            candidate.mutate(types, mutation_rate=0.4)

        print(f"CANDIDATES AFTER MUTATION: {crossover_population}")
        # Evaluate Fitness Function on New population
        SharedStatementFitness().evaluate_on(new_population)


if __name__ == "__main__":
    # src = inspect.getsource(testable)
    # tree = ast.parse(src)
    # # f_token: ast.FunctionDef = tree.body[0]
    # # f_token.
    # constants = find_constants(tree)
    # print(split_and_sort_constants(constants))

    gen = GeneticTestGenerator(random_candidate_count=3, interesting_chance=0.3)
    # Access supported_types from the genetic_generator
    supported_types = gen.supported_types

    population_int = gen.create_population_for(testable_int)
    population_float = gen.create_population_for(testable_float)
    population_str = gen.create_population_for(testable_str)

    for pop, name in zip([population_int, population_float, population_str], ["INT", "FLOAT", "STR"]):
        print(f"===== CURRENTLY TESTING TYPE {name} =====")
        preform_genetic_testing(pop, supported_types)
