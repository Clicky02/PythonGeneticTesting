from types import GenericAlias
from genetic_alg.types.type_info import GenericTypeInfo, TypeInfo


class TypeRegistry:
    available_types: dict[type | GenericAlias, TypeInfo]
    generic_types: dict[type, GenericTypeInfo]

    def __init__(self, types: list[TypeInfo], generics: list[GenericTypeInfo] = []) -> None:
        self.available_types = {}
        self.generic_types = {}

        for t in types:
            self.available_types[t.type] = t

        for t in generics:
            self.generic_types[t.type] = t

    def register_type(self, t: TypeInfo):
        self.available_types[t.type] = t

    def register_generic(self, t: GenericTypeInfo):
        self.generic_types[t.type] = t

    def get(self, t: type | GenericAlias) -> TypeInfo | None:
        if t in self.available_types:
            return self.available_types[t]
        elif isinstance(t, GenericAlias):
            base_type = t.__origin__
            if base_type in self.generic_types:
                generic = self.generic_types[base_type]
                arg_types = []
                for type_param in t.__args__:
                    param_info = self.get(type_param)

                    if param_info is None:
                        return None

                    arg_types.append(param_info)

                paramterized_type_info = generic.parameterize(arg_types)
                self.register_type(paramterized_type_info)
                return paramterized_type_info
        return None
