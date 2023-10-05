# teststock.py

import unittest

from stock import Stock


class TestStock(unittest.TestCase):
    def test_create(self):
        s = Stock("GOOG", 100, 490.1)
        self.assertEqual(s.name, "GOOG")
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_create_keyword(self):
        s = Stock(name="GOOG", shares=100, price=490.1)
        self.assertEqual(s.name, "GOOG")
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_cost(self):
        s = Stock("GOOG", 100, 490.1)
        self.assertEqual(s.cost, 49010)

    def test_sell(self):
        s = Stock("GOOG", 100, 490.1)
        self.assertEqual(s.shares, 100)
        s.sell(60)
        self.assertEqual(s.shares, 40)

    def test_from_row(self):
        s = Stock.from_row(("GOOG", 100, 490.1))
        self.assertEqual(s.name, "GOOG")
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_repr(self):
        s = Stock("GOOG", 100, 490.1)
        self.assertEqual(repr(s), "Stock('GOOG', 100, 490.1)")

    def test_eq(self):
        s1 = Stock("GOOG", 100, 490.1)
        s2 = Stock("GOOG", 100, 490.1)
        self.assertEqual(s1, s2)

    def test_bad_shares(self):
        s = Stock("GOOG", 100, 490.1)
        with self.assertRaises(TypeError):
            s.shares = "50"
        with self.assertRaises(ValueError):
            s.shares = -50

    def test_bad_price(self):
        s = Stock("GOOG", 100, 490.1)
        with self.assertRaises(TypeError):
            s.price = "490.1"
        with self.assertRaises(ValueError):
            s.price = -490.1

    def test_non_attr(self):
        s = Stock("GOOG", 100, 490.1)
        with self.assertRaises(AttributeError):
            s.share = 50


if __name__ == "__main__":
    unittest.main()
