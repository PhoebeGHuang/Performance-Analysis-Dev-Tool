from unittest import TestCase
from analyzer import Analyzer


class TestBigO(TestCase):
    def test_calculate(self):
        an = Analyzer("def print_constant(n):\n\tprint(\"constant\")", "n")
        self.assertEqual(an.calc.calculate(), "O(1)")

        an = Analyzer("def print_first(arr):\n\tprint(arr[0])", "len(arr)")
        self.assertEqual(an.calc.calculate(), "O(1)")

    def test_syntax_error(self):
        an = Analyzer("def syntax_error(n):\n\tprint(x)", "n")
        self.assertEqual(an.error_check.detect_syntax_errors(), True)

    def test_get_function_name(self):
        an = Analyzer("def print_constant(n):\n\tprint(\"constant\")", "n")
        self.assertEqual(an.get_function_name(), "print_constant(n)")
