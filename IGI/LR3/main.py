from errors import is_command
from menu import menu
import Task1
import Task2
import Task3
import Task4
import Task5


def program():
    while True:
        menu()
        command = is_command(input("\nEnter value: "))
        if command == 1:
            Task1.program()
        if command == 2:
            Task2.program()
        if command == 3:
            Task3.program()
        if command == 4:
            Task4.program()
        if command == 5:
            Task5.program()
        if command == 6:
            break


if __name__ == '__main__':
    program()
