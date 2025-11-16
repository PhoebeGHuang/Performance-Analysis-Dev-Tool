from unittest import TestCase
from analyzer import Analyzer


class TestErrorChecker(TestCase):
    def test_bad_syntax(self):
        an = Analyzer("test_programs/bad_syntax.py", "n", False)
        ec = an.error_check
        syntax_error = ec.detect_syntax_errors()
        self.assertTrue(ec)

    def test_good_syntax(self):
        an = Analyzer("test_programs/good_syntax.py", "n", False)
        ec = an.error_check
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)

    def test_inf_loop(self):
        an = Analyzer("test_programs/infinite_loop.py", "n", False)
        ec = an.error_check
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)
        timeout = ec.detect_infinite_loops()
        self.assertEqual(timeout, "timed_out")

    def test_mult_files(self):
        an = Analyzer("test_programs/mult.py", "n", False)
        ec = an.error_check
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)
        timeout = ec.detect_infinite_loops()
        self.assertEqual(timeout, "no_error")

    def test_runtime_err(self):
        an = Analyzer("test_programs/divide_by_zero.py", "n", False)
        ec = an.error_check
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)
        timeout = ec.detect_infinite_loops()
        self.assertEqual(timeout, "runtime_error")

    def test_inputs(self):
        an = Analyzer("test_programs/inputs.py", "n", True, [1, 5, 5])
        ec = an.error_check
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)

        timeout = ec.detect_infinite_loops()
        self.assertEqual(timeout, "no_error")

        an = Analyzer("test_programs/inputs.py", "n", True, [2, 5, 5])
        ec = an.error_check

        timeout = ec.detect_infinite_loops()
        self.assertEqual(timeout, "no_error")

        an = Analyzer("test_programs/inputs.py", "n", True, [3, 5, 0])
        ec = an.error_check

        timeout = ec.detect_infinite_loops()
        self.assertEqual(timeout, "runtime_error")
