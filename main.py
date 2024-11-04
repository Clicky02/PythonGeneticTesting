from dataclasses import dataclass

from genetic_alg.fitness.shared_statement_fitness import SharedStatementFitness
from genetic_alg.generator import GeneticTestGenerator


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
    pop = gen.create_population_for(testable)

    SharedStatementFitness().evaluate_on(pop)

    print(pop)
    print()
