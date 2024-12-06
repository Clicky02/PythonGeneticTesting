from __future__ import annotations
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
    create_random: Callable[[TypeInfo, GeneticContext], T]  # A function that creates a random instance of the type
    mutators: list[Callable[[T, TypeInfo, GeneticContext], T]]  # Functions that mutate an instance of the class
    interesting_values: list[T]  # A list of interesting values of that type (i.e. "" or 0)

    def random(self, ctx: GeneticContext) -> T:
        if random.random() < ctx.interesting_chance:
            return random.choice(self.interesting_values)
        return self.create_random(self, ctx)

    def mutate(self, val: T, ctx: GeneticContext):
        mutation_function = random.choice(self.mutators)
        return mutation_function(val, self, ctx)


@dataclass
class GenericTypeInfo(Generic[T]):
    """
    Dataclass with the necessary information needed to use a type with our genetic tester/
    """

    type: Type[T]  # The base type
    generic_args: int  # number of generic arguments
    create_random: Callable[
        [TypeInfo, list[TypeInfo], GeneticContext], T
    ]  # A function that creates a random instance of the type
    mutators: list[
        Callable[[T, TypeInfo, list[TypeInfo], GeneticContext], T]
    ]  # Functions that mutate an instance of the class
    interesting_values: list[T]  # A list of interesting values of that type (i.e. "" or 0)

    def parameterize(self, types: list[TypeInfo]) -> TypeInfo:
        assert len(types) == self.generic_args, "tried using a generic type with an incorrect number of type arguments"

        def create_random(type_info: TypeInfo, ctx: GeneticContext):
            return self.create_random(type_info, types, ctx)

        mutators = []
        for mut in self.mutators:

            def mutator(val, type_info: TypeInfo, ctx: GeneticContext):
                return mut(val, type_info, types, ctx)

            mutators.append(mutator)

        parameterized_type = GenericAlias(self.type, *[info.type for info in types])
        return TypeInfo(parameterized_type, create_random, mutators, self.interesting_values)
