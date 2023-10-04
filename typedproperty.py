# typedproperty.py


# Unable to do Exercise 5.4c: eliminating names from class definition using
# __set_name__ (which only works for class definitions, not closures?)


def typedproperty(name, expected_type):
    private_name = "_" + name

    @property
    def value(self):
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f"Expected {expected_type}")
        setattr(self, private_name, val)

    return value


def String(attr):
    return typedproperty(attr, str)


def Integer(attr):
    return typedproperty(attr, int)


def Float(attr):
    return typedproperty(attr, float)


class Stock:
    name = String("name")
    shares = Integer("shares")
    price = Float("price")

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
