from abc import ABC, abstractmethod
import math
import numpy as np
from matplotlib import pyplot as plt


class GeometricFigure(ABC):
    @abstractmethod
    def calculate_area(self):
        pass


class Color:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color


class Rhombus(GeometricFigure):
    figure = "Ромб"

    def __init__(self, side, angle, color):
        self.color = Color(color)
        self._side = side
        self._angle = angle

    def calculate_area(self):
        """Calculate the area of rhombus. """
        return self._side ** 2 * math.sin(math.radians(self._angle))

    def get_info(self):
        """Print info about the figure. """
        return "{type} {color} цвета со стороной {side} и углом {angle} градусов".format(
            type=self.figure,
            color=self.color.color,
            side=self._side,
            angle=self._angle
        )

    def plot(self):

        half_diagonal = self._side / 2 / np.sin(np.radians(self._angle / 2))
        x = [0, self._side/2, 0, -self._side/2, 0]
        y = [half_diagonal, 0, -half_diagonal, 0, half_diagonal]

        angle_rad = np.radians(self._angle)
        x_rot = [xi * np.cos(angle_rad) - yi * np.sin(angle_rad) for xi, yi in zip(x, y)]
        y_rot = [xi * np.sin(angle_rad) + yi * np.cos(angle_rad) for xi, yi in zip(x, y)]

        plt.plot(x_rot, y_rot, color=self.color.color)
        plt.fill(x_rot, y_rot, color=self.color.color, alpha=0.4)

        plt.axis('equal')
        plt.title(input("Подпись графика: "))
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()


def is_command(value: str) -> int:
    """Checks the value to be between 0 and 4. """
    while True:
        try:
            value = int(value)
            if 0 < value < 4:
                return value
            value = input("Value should be between 0 and 4, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_angle(value: str) -> float:
    """Checks the value to be between 0 and 90. """
    while True:
        try:
            value = float(value)
            if 0 < value < 90:
                return value
            value = input("Angle should be acute, input angle: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_side(value: str) -> float:
    """Checks the value to be greater than 0. """
    while True:
        try:
            value = float(value)
            if value > 0:
                return value
            value = input("Side should be greater than 0, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_color(value: str) -> str:
    while True:
        if value in ['blue', 'black', 'pink', 'red', 'green', 'yellow', 'orange']:
            return value
        value = input("Color should be blue, black, pink, red, green, yellow, orange, input value: ")


def menu() -> None:
    """Menu for user input. """
    print("\n1: Input the values")
    print("2: Get info about a rhombus")
    print("3: Exit\n")


def main():
    rhombus = None
    while True:
        menu()
        command = is_command(input("Enter value: "))
        if command == 1:
            side = is_side(input("Enter the length of the side of the rhombus: "))
            angle = is_angle(input("Enter the angle of the rhombus in degrees: "))
            color = is_color(input("Enter diamond color: "))
            rhombus = Rhombus(side, angle, color)
        if command == 2:
            if rhombus is None:
                print("\nFigure not found, please try again")
                continue
            print("Area of a rhombus:", rhombus.calculate_area())
            print(rhombus.get_info())
            rhombus.plot()
            with open("info.txt", "w") as file:
                file.write("Area of a rhombus: {}\n".format(rhombus.calculate_area()))
                file.write("{}\n".format(rhombus.get_info()))
        if command == 3:
            break
