from typing import override

import coverage
from genetic_alg.fitness.interface import IFitness
from genetic_alg.population import Population
from genetic_alg.util import suppressPrint


class SharedStatementFitness(IFitness):
    """
    A fitness function that uses statement coverage except the fitness
    gained for each statement is split between all candidates that executed
    that statement.
    """

    @override
    def evaluate_on(self, population: Population):
        cov = coverage.Coverage()

        candidates = population.candidates
        target = population.target
        details = population.target_details

        coverage_by_candidate: list[list[int]] = [None] * len(candidates)  # type: ignore
        with suppressPrint():
            for i in range(len(candidates)):
                candidate = candidates[i]
                cov.erase()

                args = candidate.args(details)
                kwargs = candidate.kwargs(details)

                cov.start()
                try:
                    target(*args, **kwargs)
                except:
                    ...
                cov.stop()

                lines = cov.get_data().lines(details.file)

                if lines != None:
                    candidate.lines_executed = set(lines)
                    coverage_by_candidate[i] = lines

        line_run_counts = {}
        for line in details.executable_lines:
            if line > details.first_line and line <= details.last_line:
                line_run_counts[line] = 0

        for cov in coverage_by_candidate:
            for line in cov:
                if line > details.first_line and line <= details.last_line:
                    if line in line_run_counts:
                        line_run_counts[line] += 1
                    else:
                        # This is accounting for a difference between the executable lines output
                        # and the executed lines ouput. In certain cases, the executed line will
                        # be below the executable line outputted by the coverage library
                        while line > details.first_line:
                            line -= 1
                            if line in line_run_counts:
                                line_run_counts[line] += 1
                                break

        population.total_fitness = 0
        for i in range(len(candidates)):
            candidate = candidates[i]
            candidate.fitness = 0

            for line in coverage_by_candidate[i]:
                if line in line_run_counts:
                    candidate.fitness += 1 / line_run_counts[line]

            population.total_fitness += candidate.fitness

        lines_not_run = [line for line, run_count in line_run_counts.items() if run_count == 0]

        population.coverage = (len(line_run_counts) - len(lines_not_run)) / len(line_run_counts)
        population.lines_not_executed = lines_not_run
