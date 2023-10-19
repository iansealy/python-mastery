# structure.py
import sys

from validate import Validator, validated


class Structure:
    _types = ()

    @staticmethod
    def _init():
        locs = sys._getframe(1).f_locals
        self = locs.pop("self")
        for name, val in locs.items():
            setattr(self, name, val)

    def __setattr__(self, name, value):
        if not name.startswith("_") and name not in self._fields:
            raise AttributeError(f"No attribute {name}")
        super().__setattr__(name, value)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.shares!r}, {self.price!r})"

    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

    @classmethod
    def create_init(cls):
        argstr = ",".join(cls._fields)
        code = f"def __init__(self, {argstr}):\n"
        for name in cls._fields:
            code += f"    self.{name} = {name}\n"
        locs = {}
        exec(code, locs)
        cls.__init__ = locs["__init__"]

    @classmethod
    def from_row(cls, row):
        rowdata = [func(val) for func, val in zip(cls._types, row)]
        return cls(*rowdata)


def validate_attributes(cls):
    validators = []
    types = []
    for name, val in vars(cls).items():
        if isinstance(val, Validator):
            validators.append(val)
            if hasattr(val, "expected_type"):
                types.append(val.expected_type)
        elif hasattr(val, "__annotations__"):
            for name2, val2 in val.__annotations__.items():
                if issubclass(val2, Validator):
                    setattr(cls, name, validated(val))

    cls._fields = [val.name for val in validators]
    cls._types = types

    cls.create_init()

    return cls


def typed_structure(clsname, **validators):
    cls = type(clsname, (Structure,), validators)
    return cls
