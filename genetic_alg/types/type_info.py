from dataclasses import dataclass
import random
from typing import Callable, Generic, Type, TypeVar

T = TypeVar("T")


@dataclass
class TypeInfo(Generic[T]):
    """
    Dataclass with the necessary information needed to use a type with our genetic tester/
    """

    type: Type[T]  # The type itself
    create_random: Callable[[], T]  # A function that creates a random instance of the type
    mutators: list[Callable[[T], T]]  # Functions that mutate an instance of the class
    interesting_values: list[T]  # A list of interesting values of that type (i.e. "" or 0)

    def get_random_interesting(self) -> T:
        return random.choice(self.interesting_values)
