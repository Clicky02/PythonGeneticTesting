from dataclasses import dataclass
from itertools import product
from math import ceil
import random
from types import GenericAlias
from typing import Any, Callable
from genetic_alg.candidate import Candidate
from genetic_alg.fitness.interface import IFitness
from genetic_alg.parsing.parameter import ParameterDetail
from genetic_alg.parsing.function import FunctionDetails
from genetic_alg.population import Population
from genetic_alg.selection.interface import ISelection
from genetic_alg.types.type_info import TypeInfo
from genetic_alg.types.basic import basic_type_infos

@dataclass
class GenerationResult:
    population: Population
    generations: int
    all_populations: list[Population] | None

class GeneticTestGenerator:
    """
    The main way to use our genetic testing library.
    """

    def __init__(
        self,
        fitness_algorithm: IFitness,
        selection_strategy: ISelection,
        elite_count: int = 0,
        percent_candidates_preserved: float = 0,
        mutation_rate: float = 0.05,
        random_candidate_count: int = 10,
        interesting_chance: float = 0.3,
        supported_types: dict[type | GenericAlias, TypeInfo] = basic_type_infos
    ) -> None:
        self.fitness_algorithm = fitness_algorithm
        self.selection_strategy = selection_strategy
        self.elite_count = elite_count
        self.percent_candidates_preserved = percent_candidates_preserved
        self.mutation_rate = mutation_rate
        self.random_candidate_count = random_candidate_count
        self.interesting_chance = interesting_chance
        self.supported_types = supported_types

    def run(self, target: Callable, generations: int, print_progress: bool = True) -> GenerationResult:
        return self.run_until(target, lambda gens, pop: gens >= generations, print_progress)

    def run_until(self, target: Callable, stop_condition: Callable[[int, Population], bool], print_progress: bool = True) -> GenerationResult:
        population = self.create_population_for(target)
        self.fitness_algorithm.evaluate_on(population)

        if print_progress:
            print(f"Initial Population has fitness={population.total_fitness}, coverage={population.coverage}")

        gen = 0
        best_population = population
        populations = [population]
        while not stop_condition(gen, population):
            gen += 1

            new_population = self.get_next_population(population)
            self.mutate_population(new_population)
            self.fitness_algorithm.evaluate_on(population)

            if new_population.coverage >= best_population.coverage:
                best_population = new_population

            if print_progress:
                print(f"Generation {gen} has fitness={population.total_fitness}, coverage={population.coverage}")

            populations.append(new_population)
            population = new_population

        return GenerationResult(best_population, gen, populations)

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

        return Population(population.target, population.target_details, new_candidates, self.supported_types)

    def mutate_population(self, population: Population):
        for c in population.candidates:
            for i in range(len(c.arg_values)):
                if random.random() < self.mutation_rate:
                    value = c.arg_values[i]
                    value_type = population.target_details.args[i].type

                    # Get the TypeInfo for the value's type
                    if value_type in self.supported_types:
                        type_info = self.supported_types[value_type]

                        # Choose a mutation function at random
                        mutation_function = random.choice(type_info.mutators)

                        # Apply the mutation function to the value
                        mutated_value = mutation_function(value)

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

        for param in fdetails.args:
            if param.type not in self.supported_types:
                raise Exception(f"Function contains unsupported type '{param.type}'")

        # for _ in range(self.population_size):
        #     candidates.append(signature.create_empty_candidate())

        interesting_vals_by_arg = [self.supported_types[param.type].interesting_values for param in fdetails.args]
        interesting_value_candidates = [Candidate(list(combo)) for combo in product(*interesting_vals_by_arg)]

        rand_candidates: list[Candidate] = [
            self.create_random_candidate(fdetails) for _ in range(self.random_candidate_count)
        ]

        return Population(target, fdetails, interesting_value_candidates + rand_candidates, self.supported_types)

    def create_random_candidate(self, fdetails: FunctionDetails):
        """
        Randomly creates a candidate for a target function
        """
        candidate_args = []
        for param in fdetails.args:
            candidate_args.append(self.create_random_value(param))
        return Candidate(candidate_args)

    def create_random_value(self, param: ParameterDetail):
        """
        Randomly creates a value for a function parameter
        """

        type_info = self.supported_types[param.type]
        if random.random() < self.interesting_chance:
            return type_info.get_random_interesting()
        return type_info.create_random()
