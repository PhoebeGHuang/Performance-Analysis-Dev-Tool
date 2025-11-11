import subprocess
import py_compile


class ErrorChecker:

    def __init__(self, program):
        self.program = program  # program is a subprocess
        self.err = ""

    def detect_syntax_errors(self):
        """Detects syntax errors without having to run the program"""

        try:
            print(self.program)
            py_compile.compile(self.program, doraise=True)
            return False  # program contains no syntax errors

        except py_compile.PyCompileError as err:
            self.err = err
            return True  # syntax error exists

    def detect_infinite_loops(self, needs_input=False, inputs=[], timeout=1):
        """Checks if program hangs for too long"""

        try:
            # check if user program needs inputs before running
            if needs_input:
                input_string = "\n".join(str(x) for x in inputs) + "\n"
                result = subprocess.run(
                    ["python", self.program],
                    input=input_string,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            else:
                result = subprocess.run(
                    ["python", self.program],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            if result.returncode != 0:
                self.err = result.stderr
                return "runtime_error"

            print("Program executed successfully")
            return "no_error"

        except subprocess.TimeoutExpired:
            self.err = "Timed out!\n Fix any infinite loops or other similar issues!"
            return "timed_out"

        except Exception as err:
            self.err = err
            return "unexpected_error"

    def change_program(self, new_program):
        self.program = new_program
