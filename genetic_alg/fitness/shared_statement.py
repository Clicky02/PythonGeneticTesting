from typing import override

import coverage
from genetic_alg.fitness.interface import IFitness
from genetic_alg.population import Population


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
        for i in range(len(candidates)):
            candidate = candidates[i]
            cov.erase()

            args = candidate.args(details)
            kwargs = candidate.kwargs(details)

            cov.start()
            target(*args, **kwargs)
            cov.stop()

            lines = cov.get_data().lines(details.file)

            if lines != None:
                coverage_by_candidate[i] = lines

        _, executable_lines, *_ = cov.analysis2(details.file)

        lines_run = {}
        for line in executable_lines:
            if line > details.first_line and line < details.last_line:
                lines_run[line] = 0

        for cov in coverage_by_candidate:
            for line in cov:
                if line > details.first_line and line < details.last_line:
                    lines_run[line] += 1

        population.total_fitness = 0
        for i in range(len(candidates)):
            candidate = candidates[i]
            candidate.fitness = 0

            for line in coverage_by_candidate[i]:
                if line in lines_run:
                    candidate.fitness += 1 / lines_run[line]

            population.total_fitness += candidate.fitness

        population.coverage = sum(run_count != 0 for run_count in lines_run.values()) / len(lines_run)
