import numpy as np


class Matrix:
    def __init__(self, n: int, m: int) -> None:
        self._matrix = np.random.randint(0, 100, (n, m))
        self._dimensions = (n, m)

    def __str__(self) -> str:
        return str(self._matrix)

    @property
    def dimensions(self) -> tuple:
        return self._dimensions

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix

    @staticmethod
    def from_array(array: list) -> 'Matrix':
        """Converting an Array to a Matrix. """
        m = Matrix(0, 0)
        m._matrix = np.array(array)
        m._dimensions = m.matrix.shape
        return m

    def operation(self, func) -> np.ndarray:
        """Returns the result of the function. """
        return func(self._matrix)


class UpdateMatrix(Matrix):
    def __init__(self, n: int, m: int, threshold: float) -> None:
        super().__init__(n, m)
        self._threshold = threshold
        self._filtered_elements = None

    def filter_elements(self) -> np.ndarray:
        """Filters the elements of the matrix. """
        self._filtered_elements = self.matrix[np.abs(self._matrix) > self._threshold]
        return self._filtered_elements

    def count_filtered_elements(self) -> int:
        """Counts the number of filtered. """
        if self._filtered_elements is None:
            self.filter_elements()
        return len(self._filtered_elements)

    def median_of_filtered(self) -> tuple:
        """Finds the median of the filtered elements. """
        if self._filtered_elements is None:
            self.filter_elements()
        return np.median(self._filtered_elements), self.calculate_median_manually()

    def calculate_median_manually(self):
        """Calculates the median of the filtered elements. """
        sorted_elements = np.sort(self._filtered_elements)
        mid = len(sorted_elements) // 2
        if len(sorted_elements) % 2 == 0:
            return (sorted_elements[mid - 1] + sorted_elements[mid]) / 2
        return sorted_elements[mid]


def is_command(value: str) -> int:
    """Checks the value to be between 0 and 3. """
    while True:
        try:
            value = int(value)
            if 0 < value < 3:
                return value
            value = input("Value should be between 0 and 3, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_size(value: str) -> int:
    """ Checks the value to make sure it is greater than 0. """
    while True:
        try:
            value = int(value)
            if value > 0:
                return value
            value = input("Value should be greater than 1, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_value(value: str) -> float:
    """ Checks the value to make sure it is greater than 0. """
    while True:
        try:
            value = float(value)
            if value > 0:
                return value
            value = input("Value should be greater than 0, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def menu() -> None:
    """Menu for user input. """
    print("\n1: Start program")
    print("2: Exit\n")


def main():
    while True:
        menu()
        command = is_command(input("Enter value: "))
        if command == 1:
            n, m = is_size(input("Enter n: ")), is_size(input("Enter m: "))
            ths = is_value(input("Enter threshold: "))
            mat = UpdateMatrix(n, m, ths)
            print('Matrix: \n', mat)
            print(f"\nFiltered elements: {mat.filter_elements()}")
            print(f"\nCount of filtered elements: {mat.count_filtered_elements()}")
            print(f"\nMedians: {mat.median_of_filtered()}")
        if command == 2:
            break
