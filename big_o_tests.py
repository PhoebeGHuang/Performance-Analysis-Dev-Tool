from unittest import TestCase
from analyzer import Analyzer


class TestBigO(TestCase):
    def test_calculate_O_1(self):
        an = Analyzer("O(1)_time.py", "n", False)
        self.assertEqual("$O(1)$", an.calc.calculate())

    def test_calculate_O_n(self):
        an = Analyzer("O(n)_time.py", "n", False)
        self.assertEqual("$O(n)$", an.calc.calculate())

    def test_calculate_O_n2(self):
        an = Analyzer("O(n^2)_time.py", "n", False)
        self.assertEqual("$O(n^2)$", an.calc.calculate())

    def test_calculate_O_n3(self):
        an = Analyzer("O(n^3)_time.py", "n", False)
        self.assertEqual("$O(n^3)$", an.calc.calculate())
