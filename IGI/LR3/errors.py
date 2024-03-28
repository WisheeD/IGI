def is_command(value):
    """
    Checks the value to be between 0 and 7
    """
    while True:
        try:
            value = int(value)
            if 0 < value < 7:
                return value
            value = input("Value should be between 0 and 7, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")
