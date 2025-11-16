import subprocess
import py_compile
import importlib.util
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

        self.error_check = self.ErrorChecker(program, needs_input, self.input_string)
        self.calc = self.BigOCalculator(program, n, needs_input, self.input_string)

    class ErrorChecker:
        def __init__(self, program, needs_input, input_string):
            self.program = program
            self.needs_input = needs_input
            self.input_string = input_string
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

        def detect_infinite_loops(self, timeout=1):
            """Checks if program hangs for too long"""

            try:
                # check if user program needs inputs before running
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

    class BigOCalculator:

        def __init__(self, program, n, needs_input, input_string):
            self.program = program
            self.n = n
            self.needs_input = needs_input
            self.input_string = input_string
            self.time_data = None  # times are in ns

        def calculate(self):
            """Returns a string in LaTeX format showing Big-O time complexity of program"""

            spec = importlib.util.spec_from_file_location("user_program", self.program)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            vals = self.__generate_variable_vals()  # generate values for testing main()
            time_vals = np.empty(len(vals))  # create an empty NumPy array

            if self.needs_input:  # time execution, taking best of 5 executions
                with open(self.program, mode='r') as prog_file:  # read in user program
                    code = prog_file.read()
                code = 'import sys\n' + code  # modify all assignments of n to equal a command line argument
                pattern = re.compile(f"\\b{self.n}\\s+=\\s+.+")
                code = pattern.sub(f"{self.n} = int(sys.argv[1])", code)
                with open(self.program[:-3] + "_copy.py", mode='w') as prog_file_copy:  # create temporary copy for analysis
                    prog_file_copy.write(code)
                for i in range(len(vals)):  # for each value of n, run the program
                    time_vals[i] = min(timeit.repeat(lambda: subprocess.run(["python", self.program[:-3] + "_copy.py", str(vals[i])],
                                                                            input=self.input_string,
                                                                            capture_output=True,
                                                                            text=True
                                                                            ),
                                                     timer=time.perf_counter_ns,
                                                     repeat=5,
                                                     number=1)
                                       )
                os.remove(self.program[:-3] + "_copy.py")

            else:  # time execution, taking best of 5 executions
                for i in range(len(vals)):  # for each value of n, run the program
                    module.n = vals[i]
                    time_vals[i] = min(timeit.repeat(lambda: module.main(),
                                                     timer=time.perf_counter_ns,
                                                     repeat=5,
                                                     number=1)
                                       )

            self.time_data = np.column_stack((vals, time_vals))  # create 2D NumPy array for plotting

            vals = vals.reshape(-1, 1)  # reshape inputs array for regression
            best_adj_r2 = -1  # track the adjusted R^2 to determine the best-fitting degree of polynomial
            best_degree = None
            best_model = None

            for degree in range(1, 6):  # try polynomial degrees between 0-5 inclusive
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
                    best_model = model

            if best_adj_r2 < 0.5:  # runtime is poorly correlated with n
                return "$O(1)$"

            degree = 1
            highest_coef = 0  # find poly term with largest coefficient
            for i in range(1, len(best_model.coef_)):
                if best_model.coef_[i] > highest_coef:
                    degree = i
                    highest_coef = best_model.coef_[i]

            if degree == 1:
                return "$O(n)$"
            else:
                return f"$O(n^{degree})$"

        def get_time_data(self):
            """Returns time data for plotting"""
            if self.time_data is not None:
                return self.time_data
            else:
                return [[]]

        def __generate_variable_vals(self):
            """Returns values to be used for variable being modified"""
            return np.array([5, 7, 10, 15, 20, 30, 40, 60, 80, 120, 160, 240, 320])
