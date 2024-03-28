# Program: Find the sum of the negative elements of a list and
# the product of the elements located between the max and min elements
# Version: 1.0
# Author: Troshko A.
# Date: 18.03.2024


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
            value = float(value)
            return value
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def get_list(size: int):
    """
    Returns the sequence of numbers
    """
    new_list = list()
    for _ in range(size):
        number = is_value(input("Enter a number: "))
        new_list.append(number)
    return new_list


def get_size():
    """
    Returns a number that will be the size of the list
    """
    return is_size(input("Enter the size: "))


def generator(size: int):
    """
    Returns a list of sequences
    """
    for _ in range(size):
        size_list = is_size(input("Enter the size of list: "))
        yield get_list(size_list)


def calculate_sum(numbers: list):
    """
    Returns the sum of negative numbers
    """
    return sum(num for num in numbers if num < 0)


def calculate_product(numbers: list):
    """
    Returns the product of numbers between the maximum and minimum elements
    """
    min_index, max_index = numbers.index(min(numbers)), numbers.index(max(numbers))
    result = 1
    if max_index < min_index:
        for i in range(max_index + 1, min_index):
            result *= numbers[i]
        return result
    elif max_index > min_index:
        for i in range(min_index + 1, max_index):
            result *= numbers[i]
        return result
    return numbers[0]


def output(numbers: list):
    """
    Returns the result
    """
    print(f"\nSum of negative numbers: {calculate_sum(numbers)}")
    print(f"Product of numbers: {calculate_product(numbers)}")


def output_several_series(*lists: list):
    """
    Returns the result for each strings
    """
    for numbers in lists:
        output(numbers)


def menu():
    """
    Returns menu
    """
    print("\n1: Complete task for one series numbers")
    print("2: Complete task for several series numbers")
    print("3: Exit\n")


def program():
    """
    Returns the context menu
    """
    while True:
        menu()
        command = is_command(input("\nEnter a value: "))
        if command == 1:
            size = get_size()
            numbers = get_list(size)
            output(numbers)
        if command == 2:
            size_series = get_size()
            numbers = generator(size_series)
            output_several_series(*numbers)
        if command == 3:
            break
