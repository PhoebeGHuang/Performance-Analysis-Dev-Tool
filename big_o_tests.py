from unittest import TestCase
from analyzer import Analyzer


class TestBigO(TestCase):
    def test_calculate(self):
        an = Analyzer("""
        def print_constant(n):
            print(\"constant\")
        def main():
            n = 1
            print_constant(n)
            """,
                      "n", False)
        self.assertEqual(an.calc.calculate(), "$O(1)$")

        an = Analyzer("""
        def main():
            n = 1
            for i in range(len(n)):
                print(n)
        """,
                      "n", False)
        self.assertEqual(an.calc.calculate(), "$O(n)$")

        an = Analyzer("""
        def main():
            n = 1
            for i in range(len(n)):
                for j in range(len(n)):
                    print(n)
        """,
                      "n", False)
        self.assertEqual(an.calc.calculate(), "$O(n^2)$")

        an = Analyzer("""
                def main():
                    n = 1
                    for i in range(len(n)):
                        for j in range(len(n)):
                            for k in range(len(n)):
                                print(n)
                """,
                      "n", False)
        self.assertEqual(an.calc.calculate(), "$O(n^3)$")
