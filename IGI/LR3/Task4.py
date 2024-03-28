# Program: Determine the number of words in a line, find the longest word and its serial number, print every odd word
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


def initialize():
    """
    Returns the string
    """
    return input("Enter the string: ")


def get_size():
    """
    Returns a number that will be the size of the list
    """
    return is_size(input("Enter the size: "))


def generator(size: int):
    """
    Returns a sequence of strings
    """
    for _ in range(size):
        yield initialize()


def greatest_word(string: str):
    """
    Returns the longest word and its ordinal number
    """
    great_word = max(string.split(" "), key=lambda x: len(x))
    return great_word, string.split().index(great_word) + 1


def odd_words(string: str):
    """
    Returns even words
    """
    return string.split(" ")[::2]


def decorator_function(func):
    """
    Decorator for function 'num_words'
    """
    def wrapper(args):
        result = func(args)
        print(f"\nNumber of words in string: ", end='')
        return result
    return wrapper


@decorator_function
def num_words(string):
    """
    Returns the number of words in the string
    """
    return len(string.split(" ")[:])


def output(string: str):
    """
    Returns the result
    """
    print(f"{num_words(string)}")
    word, index = greatest_word(string)
    print(f"The greatest word is '{word}' with index number {index}")
    print(f"Odd words: {" ".join(odd_words(string))}\n")


def output_several_words(*strings: str):
    """
    Returns the result for each string
    """
    for string in strings:
        output(string)


def menu():
    """
    Returns menu
    """
    print("\n1: Complete task for string")
    print("2: Complete task for strings")
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
            output(string)
        if command == 2:
            size = get_size()
            strings = generator(size)
            output_several_words(*strings)
        if command == 3:
            break
