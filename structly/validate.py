# validate.py

import decimal
import inspect
from functools import wraps


class Validator:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)

    # Collect all derived classes into a dict
    validators = {}

    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls


class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f"Expected {cls.expected_type}")
        return super().check(value)


_typed_classes = [
    ("Integer", int),
    ("Float", float),
    ("Complex", complex),
    ("Decimal", decimal.Decimal),
    ("List", list),
    ("Bool", bool),
    ("String", str),
]

globals().update(
    (name, type(name, (Typed,), {"expected_type": ty})) for name, ty in _typed_classes
)


class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError("Must be non-empty")
        return super().check(value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


class Stock:
    _types = (str, int, float)

    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.shares!r}, {self.price!r})"

    def __eq__(self, other):
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares
        return


class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.sig = inspect.signature(func)

    def __call__(self, *args, **kwargs):
        bound = self.sig.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            self.func.__annotations__[name].check(val)
        result = self.func(*args, **kwargs)
        return result


def validated(func):
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        try:
            for name, val in bound.arguments.items():
                if name == "self":
                    continue
                func.__annotations__[name].check(val)
        except TypeError:
            errors = [
                f"    {name}: Expected {func.__annotations__[name]}"
                for name, _ in bound.arguments.items()
                if name != "self"
            ]
            raise TypeError("Bad Arguments\n" + "\n".join(errors)) from None
        retval = func(*args, **kwargs)
        try:
            if "return" in func.__annotations__:
                func.__annotations__["return"].check(retval)
        except TypeError as e:
            raise TypeError(f"Bad return: {e}") from None
        return retval

    return wrapper


def enforce(**typekwargs):
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            try:
                for name, val in typekwargs.items():
                    if name == "return_":
                        continue
                    val.check(bound.arguments[name])
            except TypeError:
                errors = [
                    f"    {name}: Expected {val}"
                    for name, val in typekwargs.items()
                    if name != "return_"
                ]
                raise TypeError("Bad Arguments\n" + "\n".join(errors)) from None
            retval = func(*args, **kwargs)
            try:
                if "return_" in typekwargs:
                    typekwargs["return_"].check(retval)
            except TypeError as e:
                raise TypeError(f"Bad return: {e}") from None
            return retval

        return wrapper

    return decorator
