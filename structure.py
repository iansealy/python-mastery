# structure.py
import sys


class Structure:
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
