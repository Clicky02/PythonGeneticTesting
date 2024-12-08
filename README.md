# `genetic_alg.py`

This is a python library created for my Advanced Software Engineering course. It provides an API for automatically generating test cases using a genetic algorithm.

## Usage

These steps were tested on Windows 10 using python version 3.12.3. The steps for other operating systems might be slightly different

### Setup

1. Clone the repository and navigate to it in the command line.
2. Ensure that you have python version 3.12 installed.
3. Create a virtual environment:

```sh
python -m venv .venv
```

4. Activate the virtual environment:

```sh
./.venv/Scripts/activate
```

5. Install the required packages:

```sh
pip install -r requirement.txt
```

### Recreating the experiment

Note: The experiment discussed in our paper and presentation took multiple hours to run. We have edited `main.py` to run faster by capping the max number of generations at 10. If you want to recreate our experiment exactly, set `STOP_CONDITION = max_exec_time(5 * 60)` near the top of `main.py`. This will make it stop trying to create test inputs for a function after 5 minutes instead of 10 generations (which is how it was configured for our experiment).

1. Run the main script:

```sh
python main.py
```

### Testing new functions

The primary interface for our library is the class `GeneticTestGenerator`. This class has all the options for generating test inputs for a function.

1. Create an instance of `GeneticTestGenerator`. Configure it with any values you would like. Example:

```py
from genetic_alg.generator import GeneticTestGenerator, InitialPopulationStrategy
from genetic_alg.selection.roulette import RouletteWheelSelection
from genetic_alg.selection.tournament import TournamentSelection

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
```

2. Call 'GeneticTestGenerator.run_until()' on the function. Example:

```py
gen.run_until(my_func, lambda generations, population, start_time: generations >= 50)
```

## Experimental Artifacts

The results of our testing can be found in the `./results` folder.

## Potential Future Work

-   Experiment with different options to determine what yields the best results
-   Add a branch coverage fitness function
-   Add more supported types
