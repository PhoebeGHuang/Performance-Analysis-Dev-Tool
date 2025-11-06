import time
import timeit
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class Analyzer:

    def __init__(self, code, n):
        self.code = code

        name = self.code.removeprefix("def ")
        end = name.find("(")
        self.function_name = name[0:end]

        self.error_check = self.ErrorChecker()
        self.calc = self.BigOCalculator(code, n, self.function_name)

    def get_function_name(self):
        name = self.code.removeprefix("def ")
        end = name.find("(")
        return name[0:end]


    class ErrorChecker:

        def detect_syntax_errors(self):
            return None

        def detect_infinite_loops(self):
            return None

    class BigOCalculator:

        def __init__(self, code, n, function_name):
            self.code = code
            self.function_name = function_name
            self.n = n
            self.time_data = None  # times are in ns

        def calculate(self):
            inputs = self.__generate_inputs()
            time_vals = np.empty(len(inputs))
            # works for one-parameter functions
            for i in range(len(inputs)):
                code_obj = compile(self.code + "\n" + self.function_name + "(" + str(inputs[i]) + ")",
                                   "<string>", "exec")
                time_vals[i] = min(timeit.repeat(lambda: exec(code_obj),
                                                 timer=time.perf_counter_ns, repeat=5, number=10000)) / 10000
            self.time_data = np.concatenate((inputs, time_vals))

            inputs = inputs.reshape(-1, 1)
            best_degree = None
            best_adj_r2 = 0

            for degree in range(0, 10):
                poly = PolynomialFeatures(degree)
                x_poly = poly.fit_transform(inputs)
                model = LinearRegression().fit(x_poly, time_vals)

                y_pred = model.predict(x_poly)
                r2 = r2_score(time_vals, y_pred)

                n = len(time_vals)
                p = x_poly.shape[1] - 1  # exclude intercept term
                adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

                if adj_r2 > best_adj_r2:
                    best_adj_r2 = adj_r2
                    best_degree = degree

                if degree == 0:
                    return "O(1)"
                return f"$O(n^{best_degree})$"

        def get_time_data(self):
            if self.time_data is not None:
                return self.time_data
            else:
                return [-1]

        def __generate_inputs(self):
            # these numbers are too large for some functions
            return np.array([1, 10, 100, 1000, 10000])


def main():
    an = Analyzer("def print_constant(n):\n\tprint(\"constant\")", "n")
    code_obj = compile(an.code + "\nprint_constant(3)", '<string>', "exec")
    print(min(timeit.repeat(lambda: exec(code_obj), repeat=5, number=10000)))


if __name__ == "__main__":
    main()
