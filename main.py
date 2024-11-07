from dataclasses import dataclass
import itertools
from genetic_alg.fitness.shared_statement_fitness import SharedStatementFitness
from genetic_alg.generator import GeneticTestGenerator
from genetic_alg.selection.interface import ElitismSelection
from genetic_alg.population import Population


@dataclass
class A:
    a: int
    b: float
    c: str


JOHN = "ASA"


def testable(a: int, b: int):
    if a < 0:  # 2
        return 5
    pass
    pass
    if b < 10.4:  # 3
        pass
        if a > 6:  # 4
            pass
        else:
            pass
            pass
    pass
    g = A(a, 0.0, JOHN)
    return 3


if __name__ == "__main__":
    # src = inspect.getsource(testable)
    # tree = ast.parse(src)
    # # f_token: ast.FunctionDef = tree.body[0]
    # # f_token.
    # constants = find_constants(tree)
    # print(split_and_sort_constants(constants))

    gen = GeneticTestGenerator(random_candidate_count=3, interesting_chance=0.3)
    population = gen.create_population_for(testable)

    SharedStatementFitness().evaluate_on(population)

    print(f"INITIAL POPULATION: {population}"
          f"\n"
          f"INITIAL POPULATION SIZE: {len(population.candidates)}"
          f"\n")

    # Initialize the Selection Strategy
    elite_count = 2
    # initialize how many candidates from the population you want
    new_population_count = elite_count * 2
    selection_strategy = ElitismSelection(elite_count, new_population_count)

    # Run selection to create a new population
    new_population = selection_strategy.select_on(population)
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
        print(f"CROSSOVER 2: {parent2.crossover(parent1)}")
        crossover_population.append(cross1)
        crossover_population.append(cross2)

    print(f"CANDIDATES AFTER CROSSOVER: {crossover_population}")
    # Evaluate Fitness Function on New population
    SharedStatementFitness().evaluate_on(new_population)
