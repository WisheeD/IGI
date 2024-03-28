# Program: In a string entered from the keyboard, count the number of words starting with a lowercase letter
# Version: 1.0
# Author: Troshko A.
# Date: 18.03.2024


from Task2 import is_command


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


def initialize():
    """
    Returns the string
    """
    return input("Enter the string: ")


def generator(size: int):
    """
    Returns a sequence of strings
    """
    for _ in range(size):
        yield initialize()


def get_size():
    """
    Returns a number that will be the size of the list
    """
    return is_size(input("Enter the size: "))


def calculate_words(string):
    """
    Returns the number of words starting with a lowercase letter
    """
    k = [word for word in string.split(" ") if 96 < ord(word[:][0]) < 123]
    return len(k)


def calculate_several_words(*string):
    """
    Returns the number of words starting with a lowercase letter for each string
    """
    for word in string:
        k = calculate_words(word)
        yield k


def output_words(value):
    """
    Returns the result
    """
    print(f"Number of words starting with a lowercase letter: {value}")


def output_several_words(*values):
    """
    Returns the result for each string
    """
    for word in values:
        output_words(word)


def menu():
    """
    Returns menu
    """
    print("\n1: Counting a number of words starting with a lowercase letter for string")
    print("2: Counting a number of words starting with a lowercase letter for strings")
    print("3: Exit")


def program():
    """
    Returns the context menu
    """
    while True:
        menu()
        command = is_command(input("\nEnter a value: "))
        if command == 1:
            string = initialize()
            output_words(calculate_words(string))
        if command == 2:
            size = get_size()
            strings = generator(size)
            values = calculate_several_words(*strings)
            output_several_words(*values)
        if command == 3:
            break
