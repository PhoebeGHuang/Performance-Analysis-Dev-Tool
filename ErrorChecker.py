import subprocess
import py_compile


"""

IMPORTANT: 
This should be created inside Analyzer class, as running
this separately will result in user program being ran twice

"""


class ErrorChecker:
    """print statements are used for temporary debugging and will be replaced with GUI later"""

    def __init__(self, program):
        self.program = program  # program is a subprocess

    def detect_syntax_errors(self):
        """Detects syntax errors without having to run the program"""

        try:
            py_compile.compile(self.program, doraise=True)
            print("Program contains no syntax errors\n")  # print statement for testing
            return False  # program contains no syntax errors

        except py_compile.PyCompileError as err:
            print("Syntax error detected in program!")  # print statement for testing
            print(err)
            return True  # syntax error exists

    def detect_infinite_loops(self, needs_input, inputs=[], timeout=3):
        """Checks if program hangs for too long"""

        try:
            # check if user program needs inputs
            if needs_input:
                input_string = "\n".join(str(x) for x in inputs) + "\n"

                print(input_string)

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
                print("Runtime error detected!\n")
                print(result.stderr)
                return "runtime_error"

            print("Program executed successfully")
            return "no_error"

        except subprocess.TimeoutExpired:
            print("Program timed out! Fix any infinite loops or other similar issues\n")
            return "timed_out"

        except Exception as err:
            print("An unexpected error has occurred!")
            print(err)
            return "unexpected_error"

    def change_program(self, new_program):
        self.program = new_program
