import math
import matplotlib.pyplot as plt
import statistics
from prettytable import PrettyTable


class Statistics:
    def __init__(self) -> None:
        self._values = []
        self._series_results = []
        self._math_results = []

    @property
    def values(self) -> list:
        return self._values

    @property
    def series_results(self) -> list:
        return self._series_results

    @property
    def math_results(self) -> list:
        return self._math_results

    def add_data(self, value: float, series_result: float, math_result: float) -> None:
        """Adds data to the lists"""
        self.values.append(value)
        self.series_results.append(series_result)
        self.math_results.append(math_result)

    def mean(self) -> float:
        """Calculate the mean of the values."""
        return statistics.mean(self.values)

    def median(self) -> float:
        """Calculate the median of the values. """
        return statistics.median(self.values)

    def mode(self) -> float:
        """Calculate the mode of the values. """
        return statistics.mode(self.values)

    def variance(self) -> float:
        """Calculate the variance of the values. """
        if len(self.values) < 2:
            return float('nan')
        return statistics.variance(self.values)

    def std(self) -> float:
        """Calculate the standard deviation of the values. """
        if len(self.values) < 2:
            return float('nan')
        return statistics.stdev(self.values)

    def plot_results(self) -> None:
        """Plot the results of the calculations. """
        plt.figure(figsize=(10, 5))
        plt.plot(self.values, self.series_results, 'bo-', label='Taylor Series Approximation')
        plt.plot(self.values, self.math_results, 'r', label='Math Module Computation')
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.title('Function Approximations')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.grid(True)
        plt.annotate(f'Mean: {round(self.mean())}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12,
                     horizontalalignment='left', verticalalignment='top')
        plt.annotate(f'Median: {round(self.median())}', xy=(0.05, 0.90), xycoords='axes fraction', fontsize=12,
                     horizontalalignment='left', verticalalignment='top')
        plt.annotate(f'Mode: {round(self.mode())}', xy=(0.05, 0.85), xycoords='axes fraction', fontsize=12,
                     horizontalalignment='left', verticalalignment='top')
        variance_value = self.variance()
        if not math.isnan(variance_value):
            plt.annotate(f'Variance: {round(variance_value)}', xy=(0.05, 0.80), xycoords='axes fraction', fontsize=12,
                         horizontalalignment='left', verticalalignment='top')
        else:
            plt.annotate('Variance: Not computable', xy=(0.05, 0.80), xycoords='axes fraction', fontsize=12,
                         horizontalalignment='left', verticalalignment='top')
        std_value = self.std()
        if not math.isnan(std_value):
            plt.annotate(f'Std: {round(std_value)}', xy=(0.05, 0.75), xycoords='axes fraction', fontsize=12,
                         horizontalalignment='left', verticalalignment='top')
        else:
            plt.annotate('Std: Not computable', xy=(0.05, 0.75), xycoords='axes fraction', fontsize=12,
                         horizontalalignment='left', verticalalignment='top')
        plt.savefig('function_approximations.png')
        plt.show()


table = PrettyTable()
stat = Statistics()


def is_size(value) -> int:
    """ Checks the value to make sure it is greater than 0. """
    while True:
        try:
            value = int(value)
            if value > 0:
                return value
            value = input("Value should be greater than 0, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_eps(value) -> float:
    """ Checks the value to be between 0 and 1. """
    while True:
        try:
            value = float(value)
            if 0 < value < 1:
                return value
            value = input("Value should be between 0 and 1, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_value(value) -> float:
    """ Checks the value to make sure it is greater than 1. """
    while True:
        try:
            value = float(value)
            if value > 1:
                return value
            value = input("Value should be greater than 1, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_command(value) -> int:
    """ Checks the value to be between 0 and 4. """
    while True:
        try:
            value = int(value)
            if 0 < value < 4:
                return value
            value = input("Value should be between 0 and 4, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def get_size_tuple() -> int:
    """ Returns a number that will be the size of the list. """
    return is_size(input("Enter size of list: "))


def generator(size: int) -> tuple:
    """ Returns a sequence of numbers. """
    for _ in range(size):
        yield is_value(input("Enter values: "))


def get_list(size: int) -> tuple:
    """ Returns eps and generator. """
    return is_eps(input("Enter eps: ")), tuple(generator(size))


def get_values() -> tuple:
    """ Returns eps and value. """
    return is_eps(input("Enter eps: ")), is_value(input("Enter value: "))


def get_taylor_series_math(value: int) -> float:
    """ Returns the value of a function using a module math. """
    return math.log((value + 1) / (value - 1))


def get_taylor_series(eps: float, value: int) -> tuple:
    """ Returns the value of a function using eps. """
    s = n = 0
    a = value
    while abs(a) > eps and n < 501:
        s += a
        a = 1 / ((2 * n + 1) * value ** (2 * n + 1))
        n += 1
    s -= value
    return n, 2 * s


def add_value(eps: float, value) -> None:
    """ Adds values to the table. """
    n, s = get_taylor_series(eps, value)
    smath = get_taylor_series_math(value)
    stat.add_data(value, s, smath)
    table.field_names = ["x", "n", "F(x)", "Math F(x)", "eps"]
    table.add_row([value, n, s, smath, eps])


def add_tuple(eps: float, *args) -> None:
    """ Unpacks the tuple and calls the method 'add_value'. """
    for value in args:
        add_value(eps, value)


def output_table() -> None:
    """ Returns and clear the table. """
    print(table)
    table.clear()
    stat.plot_results()


def menu() -> None:
    """Menu for user input. """
    print("\n1: Counting a series for one numbers")
    print("2: Counting a series for several numbers")
    print("3: Exit")


def main():
    """ Returns the context menu. """
    while True:
        menu()
        command = is_command(input("\nEnter a value: "))
        if command == 1:
            eps, value = get_values()
            add_value(eps, value)
            output_table()
        if command == 2:
            size = get_size_tuple()
            eps, new_list = get_list(size)
            add_tuple(eps, *new_list)
            output_table()
        if command == 3:
            break
