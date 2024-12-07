from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import ceil
import os
import random
import time
from types import GenericAlias
from typing import Any, Callable, Hashable
from genetic_alg.context import GeneticContext
from genetic_alg.candidate import Candidate
from genetic_alg.fitness.interface import IFitness
from genetic_alg.parsing.constants import find_constants
from genetic_alg.parsing.parameter import ParameterDetail
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.population import Population
from genetic_alg.selection.interface import ISelection
from genetic_alg.types.registry import TypeRegistry
from genetic_alg.types.type_info import TypeInfo
from genetic_alg.types.basic import default_registry


@dataclass
class GenerationResult:
    population: Population
    generations: int
    population_size: int
    all_populations: list[Population] | None


class InitialPopulationStrategy(Enum):
    INTERESTING_FIRST = 0
    MIN_PERCENT_RANDOM = 1


class GeneticTestGenerator:
    """
    The main way to use our genetic testing library.
    """

    def __init__(
        self,
        fitness_algorithm: IFitness,
        selection_strategy: ISelection,
        pop_size: int = 30,  # Number of candidates in the population
        elite_count: int = 0,  # Number of elite candidates preserved each generation
        percent_candidates_preserved: float = 0,  # Percent of candidates preserved each generation
        mutation_rate: float = 0.05,  # Mutation chance per argument
        init_population_strat: InitialPopulationStrategy = InitialPopulationStrategy.INTERESTING_FIRST,  # how the initial population is chosen
        pop_random_percent: float = 0.5,  # Min percent of population to be randomly created, only used if init_population_strat is MIN_PERCENT_RANDOM
        interesting_chance: float = 0.3,  # Chance that a random value is an interesting value
        mutate_to_new_value_chance: float = 0.1,
        dynamic_interesting_values: bool = True,  # Whether to scan the function to find interesting values
        type_registry: TypeRegistry = default_registry,
    ) -> None:
        self.fitness_algorithm = fitness_algorithm
        self.selection_strategy = selection_strategy
        self.pop_size = pop_size
        self.elite_count = elite_count
        self.percent_candidates_preserved = percent_candidates_preserved
        self.mutation_rate = mutation_rate
        self.init_population_strat = init_population_strat
        self.pop_random_percent = pop_random_percent
        self.interesting_chance = interesting_chance
        self.mutate_to_new_value_chance = mutate_to_new_value_chance
        self.dynamic_interesting_values = dynamic_interesting_values
        self.type_registry = type_registry

    def run(self, target: Callable, generations: int, print_progress: bool = True) -> GenerationResult:
        return self.run_until(target, lambda gens, *_: gens >= generations, print_progress)

    def run_until(
        self, target: Callable, stop_condition: Callable[[int, Population, float], bool], print_progress: bool = True
    ) -> GenerationResult:
        population, ctx = self.create_population_for(target)
        self.fitness_algorithm.evaluate_on(population)

        gen = 0
        start_time = time.time()
        best_population = population
        populations = [population]
        while not stop_condition(gen, population, start_time):
            if print_progress:
                columns, _ = os.get_terminal_size()
                # print(population)
                message = f"generation={gen}, fitness={population.total_fitness}, coverage={population.coverage}, pop_size={len(population.candidates)}"
                print(
                    f"{message:<{columns}}",
                    sep="",
                    end="\r",
                    flush=True,
                )

            gen += 1

            new_population = self.get_next_population(population)
            self.mutate_population(new_population, ctx)
            self.fitness_algorithm.evaluate_on(new_population)

            if new_population.coverage >= best_population.coverage:
                best_population = new_population

            populations.append(new_population)
            population = new_population

        if print_progress:
            columns, _ = os.get_terminal_size()
            message = f"generations={gen}, fitness={best_population.total_fitness}, coverage={best_population.coverage}, pop_size={len(best_population.candidates)}, missed_lines={best_population.lines_not_executed}"
            print(
                f"{message:<{columns}}",
                sep="",
            )

        return GenerationResult(best_population, gen, self.pop_size, populations)

    def get_next_population(self, population: Population) -> Population:
        curr_candidates = population.candidates
        total_fitness = population.total_fitness

        pop_size = len(population.candidates)
        new_candidates = []

        elite_count = min(self.elite_count, pop_size - 1)
        if self.elite_count > 0:
            sorted_candidates = sorted(population.candidates, key=lambda candidate: candidate.fitness, reverse=True)
            new_candidates = sorted_candidates[:elite_count]

        preserved_count = int((pop_size - elite_count) * self.percent_candidates_preserved)
        for _ in range(preserved_count):
            candidate = self.selection_strategy.select_from(curr_candidates, total_fitness)
            new_candidates.append(candidate.copy())

        crossover_count = pop_size - elite_count - preserved_count
        for _ in range(ceil(crossover_count / 2)):
            parent1 = self.selection_strategy.select_from(curr_candidates, total_fitness)
            parent2 = self.selection_strategy.select_from(curr_candidates, total_fitness)
            new_candidates += parent1.crossover(parent2)

        new_candidates = new_candidates[:pop_size]

        assert len(new_candidates) == pop_size

        return Population(population.target, population.target_details, new_candidates)

    def mutate_population(self, population: Population, ctx: GeneticContext):
        for c in population.candidates:
            for i in range(len(c.arg_values)):
                if random.random() < self.mutation_rate:
                    value = c.arg_values[i]
                    value_type = population.target_details.args[i].type

                    # Get the TypeInfo for the value's type
                    type_info = self.type_registry.get(value_type)
                    if type_info is not None:
                        if random.random() < self.mutate_to_new_value_chance:
                            mutated_value = type_info.random(ctx)
                        else:
                            # Choose a mutation function at random
                            mutation_function = random.choice(type_info.mutators)

                            # Apply the mutation function to the value
                            mutated_value = mutation_function(value, type_info, ctx)

                        # print(f"Mutating {c.arg_values[i]} -> {mutated_value}")
                        c.arg_values[i] = mutated_value
                    else:
                        # Handle unsupported types if necessary
                        print(f"No TypeInfo available for type {value_type}, skipping mutation.")

    def create_population_for(self, target: Callable):
        """
        Creates an initial population given a function you want to test.
        """

        fdetails = FunctionDetails.from_func(target)
        ctx = GeneticContext(self.mutation_rate, self.interesting_chance)

        param_type_infos: list[TypeInfo] = []
        for param in fdetails.args:
            type_info = self.type_registry.get(param.type)

            if type_info is None:
                raise Exception(f"Function contains unsupported type '{param.type}'")

            param_type_infos.append(type_info)

        # for _ in range(self.population_size):
        #     candidates.append(signature.create_empty_candidate())

        if self.dynamic_interesting_values:
            constants = find_constants(target)
            ctx.interesting_values = constants

            interesting_vals_by_arg = [
                (
                    ti.interesting_values + constants.get(ti.type, [])
                    if isinstance(ti.type, GenericAlias) or not issubclass(ti.type, Hashable)  # type: ignore
                    else set(ti.interesting_values + constants.get(ti.type, []))
                )
                for ti in param_type_infos
            ]
        else:
            interesting_vals_by_arg = [ti.interesting_values for ti in param_type_infos]

        interesting_value_candidates = [Candidate(list(combo)) for combo in product(*interesting_vals_by_arg)]

        if self.init_population_strat == InitialPopulationStrategy.INTERESTING_FIRST:
            interesting_candidate_count = min(self.pop_size, len(interesting_value_candidates))
            random_candidate_count = self.pop_size - interesting_candidate_count
        elif self.init_population_strat == InitialPopulationStrategy.MIN_PERCENT_RANDOM:
            random_candidate_count = min(self.pop_size, ceil(self.pop_size * self.pop_random_percent))
            interesting_candidate_count = self.pop_size - random_candidate_count
        else:
            raise Exception("Invalid initial population strategy.")

        interesting_value_candidates = random.sample(interesting_value_candidates, interesting_candidate_count)

        rand_candidates: list[Candidate] = [
            self.create_random_candidate(fdetails, ctx) for _ in range(random_candidate_count)
        ]

        return Population(target, fdetails, interesting_value_candidates + rand_candidates), ctx

    def create_random_candidate(self, fdetails: FunctionDetails, ctx: GeneticContext):
        """
        Randomly creates a candidate for a target function
        """
        candidate_args = []
        for param in fdetails.args:
            candidate_args.append(self.create_random_value(param, ctx))
        return Candidate(candidate_args)

    def create_random_value(self, param: ParameterDetail, ctx: GeneticContext):
        """
        Randomly creates a value for a function parameter
        """

        type_info = self.type_registry.get(param.type)

        if type_info is None:
            raise Exception(f"Creating random value for unsupported type '{param.type}'")

        return type_info.random(ctx)
