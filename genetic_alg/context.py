from dataclasses import dataclass, field
from types import GenericAlias


@dataclass
class GeneticContext:
    mutation_rate: float
    interesting_chance: float
    interesting_values: dict[type | GenericAlias, list] = field(default_factory=lambda: {})
