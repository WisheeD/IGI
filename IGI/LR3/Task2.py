# Program: Organize a loop that takes integers and calculates the arithmetic mean of even numbers. End - input 1
# Version: 1.0
# Author: Troshko A.
# Date: 18.03.2024


def is_size(value):
    """
    Checks the value to make sure it is greater than 0
    """
    while True:
        try:
            value = int(value)
            if value > 0:
                return value
            value = input("Value should be greater than 0, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_value(value):
    """
    Checks if a value is a number
    """
    while True:
        try:
            value = int(value)
            return value
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def is_command(value):
    """
    Checks the value to be between 0 and 4
    """
    while True:
        try:
            value = int(value)
            if 0 < value < 4:
                return value
            value = input("Value should be between 0 and 4, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def input_numbers():
    """
    Returns a list of numbers
    """
    numbers = list()
    while True:
        try:
            number = int(input("Enter a number: "))
            if number == 1:
                break
            numbers.append(number)
        except ValueError:
            number = input("Invalid input, please enter a valid value: ")
            if number == 1:
                break
    return numbers


def get_size():
    """
    Returns a number that will be the size of the list
    """
    return is_size(input("Enter a size of list: "))


def generator():
    """
    Returns a sequence of numbers
    """
    while True:
        value = is_value(input("Enter a number: "))
        yield value
        if value == 1:
            break


def calculate_avg(args: list):
    """
    Returns the arithmetic mean of even numbers
    """
    try:
        avg = [num for num in args if num % 2 == 0]
        return sum(avg) / len(avg)
    except ZeroDivisionError:
        return None


def output_avg(args):
    """
    Returns the result
    """
    print(f"\nAverage of even numbers: {calculate_avg(args)}\n")


def menu():
    """
    Returns menu
    """
    print("\n1: Counting a avg for one series numbers")
    print("2: Counting a avg for several series numbers")
    print("3: Exit")


def program():
    """
    Returns the context menu
    """
    while True:
        menu()
        command = is_command(input("\nEnter a value: "))
        if command == 1:
            new_list = input_numbers()
            output_avg(new_list)
        if command == 2:
            size = get_size()
            for _ in range(size):
                k = generator()
                output_avg(k)
        if command == 3:
            break
