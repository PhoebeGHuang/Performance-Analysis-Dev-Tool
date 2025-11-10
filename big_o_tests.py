from unittest import TestCase
from analyzer import Analyzer


class TestBigO(TestCase):
    def test_calculate(self):
        an = Analyzer("def print_constant(n):\n\tprint(\"constant\")\ndef main():\n\tn = 1\nprint_constant(n)", "n", False)
        self.assertEqual(an.calc.calculate(), "$O(1)$")

        # an = Analyzer("def print_first(arr):\n\tprint(arr[0])\ndef main():\n\tarr = {1}\nprint_first(arr)", "len(arr)")
        # self.assertEqual(an.calc.calculate(), "$O(1)$")

    def test_syntax_error(self):
        an = Analyzer("def syntax_error(n):\n\tprint(x)", "n", False)
        self.assertEqual(an.error_check.detect_syntax_errors(), True)
