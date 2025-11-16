from unittest import TestCase
import ErrorChecker


class TestErrorChecker(TestCase):
    def test_bad_syntax(self):
        ec = ErrorChecker.ErrorChecker("test_programs/bad_syntax.py")
        syntax_error = ec.detect_syntax_errors()
        self.assertTrue(ec)

    def test_good_syntax(self):
        ec = ErrorChecker.ErrorChecker("test_programs/good_syntax.py")
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)

    def test_inf_loop(self):
        ec = ErrorChecker.ErrorChecker("test_programs/infinite_loop.py")
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)
        timeout = ec.detect_infinite_loops(needs_input=False)
        self.assertEqual(timeout, "timed_out")

    def test_mult_files(self):
        ec = ErrorChecker.ErrorChecker("test_programs/mult.py")
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)
        timeout = ec.detect_infinite_loops(needs_input=False)
        self.assertEqual(timeout, "no_error")

    def test_runtime_err(self):
        ec = ErrorChecker.ErrorChecker("test_programs/divide_by_zero.py")
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)
        timeout = ec.detect_infinite_loops(needs_input=False)
        self.assertEqual(timeout, "runtime_error")

    def test_inputs(self):
        ec = ErrorChecker.ErrorChecker("test_programs/inputs.py")
        syntax_error = ec.detect_syntax_errors()
        self.assertFalse(syntax_error)

        timeout = ec.detect_infinite_loops(needs_input=True, inputs=[1, 5, 5])
        self.assertEqual(timeout, "no_error")

        timeout = ec.detect_infinite_loops(needs_input=True, inputs=[2, 5, 5])
        self.assertEqual(timeout, "no_error")

        timeout = ec.detect_infinite_loops(needs_input=True, inputs=[3, 5, 0])
        self.assertEqual(timeout, "runtime_error")
