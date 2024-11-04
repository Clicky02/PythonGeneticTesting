from dataclasses import dataclass
from enum import Enum
import inspect
from typing import Any, Callable, Optional, Self


# Define an Enum for parameter types
class ParamKind(Enum):
    """
    What position the parameter can be in.
    """

    POSITIONAL_ONLY = "positional-only"
    POSITIONAL_OR_KEYWORD = "positional-or-keyword"
    KEYWORD_ONLY = "keyword-only"
    VAR_POSITIONAL = "variable positional (*args)"
    VAR_KEYWORD = "variable keyword (**kwargs)"


@dataclass
class ParameterDetail:
    """
    Contains useful information about a function that is necessary for testing.
    """

    name: str
    type: type
    default: Any | None
    kind: ParamKind

    @classmethod
    def from_inspect(cls, param: inspect.Parameter) -> Self:
        name = param.name

        match param.kind:
            case param.POSITIONAL_ONLY:
                param_kind = ParamKind.POSITIONAL_ONLY
            case param.POSITIONAL_OR_KEYWORD:
                param_kind = ParamKind.POSITIONAL_OR_KEYWORD
            case param.KEYWORD_ONLY:
                param_kind = ParamKind.KEYWORD_ONLY
            case param.VAR_POSITIONAL:
                param_kind = ParamKind.VAR_POSITIONAL
            case param.VAR_KEYWORD:
                param_kind = ParamKind.VAR_KEYWORD
            case _:
                raise ValueError(f"Unknown parameter kind for parameter '{name}'")

        if isinstance(param.annotation, type):
            param_type = param.annotation
        else:
            raise ValueError(f"Parameter '{name}' does not have a (valid) type signature ")

        return cls(
            name=name,
            type=param_type,
            default=param.default if param.default != inspect.Parameter.empty else None,
            kind=param_kind,
        )
