from dataclasses import dataclass
import random
from typing import Callable, Generic, Type, TypeVar

T = TypeVar("T")


@dataclass
class TypeInfo(Generic[T]):
    type: Type[T]
    create_random: Callable[[], T]
    mutators: list[Callable[[T], T]]
    interesting_values: list[T]

    def get_random_interesting(self) -> T:
        return random.choice(self.interesting_values)
