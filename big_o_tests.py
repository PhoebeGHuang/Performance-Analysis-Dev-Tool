from unittest import TestCase
from analyzer import Analyzer


class TestBigO(TestCase):
    def test_calculate(self):
        # an = Analyzer("O(1)_time.py", "n", False)
        # self.assertEqual(an.calc.calculate(), "$O(1)$")

        # an = Analyzer("O(n)_time.py", "n", False)
        # self.assertEqual(an.calc.calculate(), "$O(n)$")

        an = Analyzer("O(n^2)_time.py", "n", False)
        self.assertEqual(an.calc.calculate(), "$O(n^2)$")

        an = Analyzer("O(n^3)_time.py", "n", False)
        self.assertEqual(an.calc.calculate(), "$O(n^3)$")
