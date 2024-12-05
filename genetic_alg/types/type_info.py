from dataclasses import dataclass
import random
from types import GenericAlias
from typing import Callable, Generic, Type, TypeVar

from genetic_alg.context import GeneticContext

T = TypeVar("T")


@dataclass
class TypeInfo(Generic[T]):
    """
    Dataclass with the necessary information needed to use a type with our genetic tester/
    """

    type: Type[T] | GenericAlias  # The type itself
    create_random: Callable[[GeneticContext], T]  # A function that creates a random instance of the type
    mutators: list[Callable[[T, GeneticContext], T]]  # Functions that mutate an instance of the class
    interesting_values: list[T]  # A list of interesting values of that type (i.e. "" or 0)

    def random(self, ctx: GeneticContext) -> T:
        if random.random() < ctx.interesting_chance:
            return random.choice(self.interesting_values)
        return self.create_random(ctx)

    def mutate(self, val: T, ctx: GeneticContext):
        mutation_function = random.choice(self.mutators)
        return mutation_function(val, ctx)


@dataclass
class GenericTypeInfo(Generic[T]):
    """
    Dataclass with the necessary information needed to use a type with our genetic tester/
    """

    type: Type[T]  # The base type
    generic_args: int  # number of generic arguments
    create_random: Callable[
        [list[TypeInfo], GeneticContext], T
    ]  # A function that creates a random instance of the type
    mutators: list[Callable[[T, list[TypeInfo], GeneticContext], T]]  # Functions that mutate an instance of the class
    interesting_values: list[T]  # A list of interesting values of that type (i.e. "" or 0)

    def parameterize(self, types: list[TypeInfo]) -> TypeInfo:
        assert len(types) == self.generic_args, "tried using a generic type with an incorrect number of type arguments"

        def create_random(ctx: GeneticContext):
            return self.create_random(types, ctx)

        mutators = []
        for mut in self.mutators:

            def mutator(val, ctx: GeneticContext):
                return mut(val, types, ctx)

            mutators.append(mutator)

        parameterized_type = GenericAlias(self.type, *[info.type for info in types])
        return TypeInfo(parameterized_type, create_random, mutators, self.interesting_values)
