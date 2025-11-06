import subprocess
import py_compile


"""

IMPORTANT: 
This should be created inside BigOCalculator.get_time_data(), as
running this separately will result in user program being ran twice

"""


class ErrorChecker:
    """print statements are used for temporary debugging and will be replaced with GUI later"""

    def __init__(self, program):
        self.program = program  # program is a subprocess

    def detect_syntax_errors(self):
        """Detects syntax errors without having to run the program"""

        try:
            py_compile.compile(self.program, doraise=True)
            print("\nProgram contains no syntax errors")  # print statement for testing
            return False  # program contains no syntax errors

        except py_compile.PyCompileError as err:
            print("\nSyntax error detected in program!\n")  # print statement for testing
            print(err)
            return True  # syntax error exists

    def detect_infinite_loops(self, timeout=3):
        """Checks if program hangs for too long"""

        def valid_num(var):
            """Checks if variable can be converted to int"""
            try:
                var = int(var)
                return True
            except ValueError:
                return False

        # Ask user if program needs input
        needs_input = False
        inputs = list()

        num_inputs = input("How many inputs does your program need?")
        while not valid_num(num_inputs):
            num_inputs = input("Invalid response! How many inputs does your program need?")
        num_inputs = int(num_inputs)

        if num_inputs > 0:
            needs_input = True
            for i in range(num_inputs):
                # Check last digits of num_inputs so correct suffix is used (i.e. 1st, 2nd, 3rd)
                if 10 <= (i + 1) % 100 <= 13:
                    suffix = "th"
                elif (i + 1) % 10 == 1:
                    suffix = "st"
                elif (i + 1) % 10 == 2:
                    suffix = "nd"
                elif (i + 1) % 10 == 3:
                    suffix = "rd"
                else:
                    suffix = "th"
                required_input = input(f"What is the {i + 1}{suffix} required input in your program?")
                inputs.append(required_input)

        try:
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
                print("\nRuntime error detected!\n")
                print(result.stderr)
                return "runtime_error"

            print("\nProgram executed successfully")
            return "no_error"

        except subprocess.TimeoutExpired:
            print("\nProgram timed out! Fix any infinite loops or other similar issues")
            return "timed_out"

        except Exception as err:
            print("\nAn unexpected error has occurred!\n")
            print(err)
            return "unexpected_error"
