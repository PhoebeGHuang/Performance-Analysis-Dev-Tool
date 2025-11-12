import subprocess
import py_compile
import os
import re
import time
import timeit
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class Analyzer:

    def __init__(self, program, n, needs_input, inputs=None):
        self.program = program  # program is a filename
        self.needs_input = needs_input
        if self.needs_input:
            self.input_string = "\n".join(str(x) for x in inputs) + "\n"
        else:
            self.input_string = None

        self.error_check = self.ErrorChecker(program, n, needs_input, self.input_string)
        self.calc = self.BigOCalculator(program, n, needs_input, self.input_string)

    class ErrorChecker:
        """print statements are used for temporary debugging and will be replaced with GUI later"""

        def __init__(self, program, n, needs_input, input_string):
            self.program = program  # program is a subprocess
            self.n = n
            self.needs_input = needs_input
            self.input_string = input_string

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

        def detect_infinite_loops(self, timeout=3):
            """Checks if program hangs for too long"""

            try:
                # check if user program needs inputs
                if self.needs_input:

                    result = subprocess.run(
                        ["python", self.program],
                        input=self.input_string,
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

    class BigOCalculator:

        def __init__(self, program, n, needs_input, input_string):
            self.program = program
            self.n = n
            self.needs_input = needs_input
            self.input_string = input_string
            self.time_data = None  # times are in ns

        def calculate(self):
            """Returns a string in LaTeX format showing Big-O time complexity of program"""
            prog_file = open(self.program, mode='r')  # read in user program
            code = prog_file.read()
            prog_file.close()
            prog_file_copy = open(self.program[:-3] + "_copy.py", mode='w')  # create temporary copy for analysis

            vals = self.__generate_variable_vals()  # generate values for testing main()
            time_vals = np.empty(len(vals))  # create an empty NumPy array

            for i in range(len(vals)):  # for each value of n, run the program
                # modify all assignments of n so that n equals the input value we want to test
                # TODO: fix so that only main() is modified, not the entire file
                new_code = re.sub(f"\\b{self.n}\\s+=\\s+.+", lambda match_obj: f"{self.n} = {vals[i]}", code)
                prog_file_copy.seek(0)
                prog_file_copy.truncate()
                prog_file_copy.write(new_code)
                prog_file_copy.flush()

                if self.needs_input:  # time execution, taking best of 5 executions
                    time_vals[i] = min(timeit.repeat(lambda: subprocess.run(["python", self.program[:-3] + "_copy.py"],
                                                                            input=self.input_string,
                                                                            capture_output=True,
                                                                            text=True
                                                                            ),
                                                     timer=time.perf_counter_ns,
                                                     repeat=5,
                                                     number=1)
                                       )
                else:  # time execution, taking best of 5 executions
                    time_vals[i] = min(timeit.repeat(lambda: subprocess.run(["python", self.program[:-3] + "_copy.py"],
                                                                            capture_output=True,
                                                                            text=True
                                                                            ),
                                                     timer=time.perf_counter_ns,
                                                     repeat=5,
                                                     number=1)
                                       )

            prog_file_copy.close()
            os.remove(self.program[:-3] + "_copy.py")

            self.time_data = np.column_stack((vals, time_vals))  # create 2D NumPy array for plotting

            vals = vals.reshape(-1, 1)  # reshape inputs array for regression
            best_degree = None
            best_adj_r2 = -1  # track the adjusted R^2 to determine the best-fitting degree of polynomial

            for degree in range(0, 10):  # try polynomial degrees between 0-9 inclusive
                poly = PolynomialFeatures(degree)  # create polynomial of degree n
                x_poly = poly.fit_transform(vals)  # transform input data for regression
                model = LinearRegression().fit(x_poly, time_vals)  # fit polynomial to data

                y_pred = model.predict(x_poly)  # calculate y-values produced by fitted polynomial
                r2 = r2_score(time_vals, y_pred)  # calculate R^2 to determine accuracy of model

                n = len(time_vals)
                p = x_poly.shape[1] - 1  # exclude intercept term
                adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)  # calculated adjusted R^2

                if adj_r2 > best_adj_r2:  # keep track of degree with highest adjusted R^2
                    best_adj_r2 = adj_r2
                    best_degree = degree

            if best_degree == 0:  # return time complexity
                return "$O(1)$"
            elif best_degree == 1:
                return "$O(n)$"
            else:
                return f"$O(n^{best_degree})$"

        def get_time_data(self):
            """Returns time data for plotting"""
            if self.time_data is not None:
                return self.time_data
            else:
                return [[]]

        def __generate_variable_vals(self):
            """Returns values to be used for variable being modified"""
            return np.array([1, 2, 5, 8, 10, 20, 50, 80, 100, 200, 500])
