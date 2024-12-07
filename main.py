import itertools
from pathlib import Path
from typing import Callable

import pandas as pd
from genetic_alg.fitness.shared_statement import SharedStatementFitness
from genetic_alg.generator import GenerationResult, GeneticTestGenerator, InitialPopulationStrategy
from genetic_alg.population import Population
from genetic_alg.selection.roulette import RouletteWheelSelection
from genetic_alg.selection.tournament import TournamentSelection

# from genetic_alg.selection.elitism import ElitismSelection
from genetic_alg.stop_conditions import max_exec_time, max_generations
from genetic_alg.util import print_list
from tests import code_generator, test_funcs

POP_SIZE = 64
INTERESTING_CHANCE = 0.5
CANDIDATES_PRESERVED = 0.5
MUTATION_RATE = 0.25
NEW_VALUE_MUTATION_RATE = 0.025
STOP_CONDITION = max_generations(10)
# STOP_CONDITION = max_exec_time(5 * 60)


def create_data_dict():
    return {
        "function": [],
        "coverage": [],
        "generations": [],
        "pop_size": [],
        "missed_lines": [],
        "test_cases": [],
    }


def update_data_dict(data: dict[str, list], result: GenerationResult):
    data["function"].append(result.population.target_details.name)
    data["coverage"].append(result.population.coverage)
    data["generations"].append(result.generations)
    data["pop_size"].append(result.population_size)
    data["missed_lines"].append(result.population.lines_not_executed)
    data["test_cases"].append(result.population.candidates_as_strings())


def run_test(gen: GeneticTestGenerator, end_condition: Callable, tests: list[Callable], output_file: str | None = None):
    data = create_data_dict()

    for func in tests:
        print(f"Testing {func.__name__}...")
        result = gen.run_until(func, end_condition)
        result.population.minimize()
        update_data_dict(data, result)
        candidates = result.population.candidates_as_strings()
        print_list(candidates)
        print()

    if output_file is not None:
        path = Path(f"./results/{output_file}")
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(data).to_csv(path)


if __name__ == "__main__":

    # test_funcs = [code_generator]

    no_interesting_gen = GeneticTestGenerator(
        SharedStatementFitness(),
        TournamentSelection(),
        init_population_strat=InitialPopulationStrategy.MIN_PERCENT_RANDOM,
        pop_random_percent=1.0,
        pop_size=POP_SIZE,
        interesting_chance=0,
        percent_candidates_preserved=CANDIDATES_PRESERVED,
        mutation_rate=MUTATION_RATE,
        mutate_to_new_value_chance=NEW_VALUE_MUTATION_RATE,
        dynamic_interesting_values=False,
    )

    simple_interesting_gen = GeneticTestGenerator(
        SharedStatementFitness(),
        TournamentSelection(),
        init_population_strat=InitialPopulationStrategy.INTERESTING_FIRST,
        pop_size=POP_SIZE,
        interesting_chance=INTERESTING_CHANCE,
        percent_candidates_preserved=CANDIDATES_PRESERVED,
        mutation_rate=MUTATION_RATE,
        mutate_to_new_value_chance=NEW_VALUE_MUTATION_RATE,
        dynamic_interesting_values=False,
    )

    gen = GeneticTestGenerator(
        SharedStatementFitness(),
        TournamentSelection(),
        init_population_strat=InitialPopulationStrategy.INTERESTING_FIRST,
        pop_size=POP_SIZE,
        interesting_chance=INTERESTING_CHANCE,
        percent_candidates_preserved=CANDIDATES_PRESERVED,
        mutation_rate=MUTATION_RATE,
        mutate_to_new_value_chance=NEW_VALUE_MUTATION_RATE,
        dynamic_interesting_values=True,
    )

    for i in range(3):

        print()
        print(f"****************************************")
        print(f"STARTING NO INTERESTING TEST {i + 1}")
        print(f"****************************************")
        print()

        run_test(no_interesting_gen, STOP_CONDITION, test_funcs, f"no_interesting_{i}.csv")

        print()
        print(f"****************************************")
        print(f"STARTING SIMPLE INTERESTING TEST {i + 1}")
        print(f"****************************************")
        print()

        run_test(simple_interesting_gen, STOP_CONDITION, test_funcs, f"simple_interesting_{i}.csv")

        print()
        print(f"****************************************")
        print(f"STARTING ALL INTERESTING TEST {i + 1}")
        print(f"****************************************")
        print()

        run_test(gen, STOP_CONDITION, test_funcs, f"all_interesting_{i}.csv")
