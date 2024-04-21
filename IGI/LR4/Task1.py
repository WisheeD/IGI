import csv
import pickle


class Tree:
    def __init__(self, tree_type: str, total: int, healthy: int) -> None:
        if healthy > total:
            raise ValueError("There cannot be more healthy trees than the total number")
        self._tree_type = tree_type
        self._total = total
        self._healthy = healthy

    def __str__(self) -> str:
        return f"Type: {self.tree_type}, Total: {self.total}, Healthy: {self.healthy}"

    @property
    def tree_type(self):
        return self._tree_type

    @property
    def total(self):
        return self._total

    @property
    def healthy(self):
        return self._healthy

    @property
    def diseased(self):
        return self._total - self._healthy

    @property
    def diseased_percent(self):
        return (self.diseased - self.total) * 100 if self.total else 0

    @healthy.setter
    def healthy(self, value: int):
        if value > self._healthy:
            raise ValueError("There cannot be more healthy trees than the total number")
        self._healthy = value


class Forest:
    def __init__(self, trees: dict):
        self._trees = list()
        self.total_count = 0
        self.total_healthy_count = 0
        for tree_type, info in trees.items():
            self.add_tree(tree_type, info["total"], info["healthy"])

    @property
    def trees(self):
        return self._trees

    def add_tree(self, tree_type: str, total: int, healthy: int) -> None:
        """Add a tree to the trees list. """
        if healthy > total:
            raise ValueError("There cannot be more healthy trees than the total number")
        self._trees.append(Tree(tree_type, total, healthy))
        self.total_healthy_count += healthy
        self.total_count += total

    def total_trees_count(self) -> str:
        """Return the total number of trees in the trees list. """
        return f"\nTotal trees in forest: {self.total_count}"

    def total_healthy_trees_count(self) -> str:
        """Return the healthy number of trees in the trees list. """
        return f"\nTotal healthy trees in forest: {self.total_healthy_count}"

    def get_tree(self, tree_type: str) -> str:
        """Return the info of the tree in the trees list. """
        tree_info = list()
        for tree in self._trees:
            if tree.tree_type == tree_type:
                tree_info.append(f"\nType: {tree.tree_type}, Total: {tree.total}, Healthy: {tree.healthy}")
                return "\n".join(tree_info)
        return f"\nNo tree with type '{tree_type}'"

    def get_all_trees(self) -> str:
        """Return the all trees in the trees list. """
        return "\n".join(
            [f"Type: {tree.tree_type}, Total: {tree.total}, Healthy: {tree.healthy}" for tree in self._trees])

    def relative_diseased_percent(self) -> str:
        """Return the relative diseased percentage of the trees in the trees list. """
        return (f"\nRelative abundance (%) of diseased trees: "
                f"{(sum(tree.diseased for tree in self._trees) / self.total_count) * 100.0}")\
            if self.total_count > 0 else 0

    def relative_diseased_percent_by_type(self) -> str:
        """Return the relative diseased percentage by type of the trees in the trees list. """
        return "\n".join(
            [f"Relative abundance (%) of diseased '{tree.tree_type}': "
             f"{round(tree.diseased / tree.total * 100.0, 2)}" for tree in self._trees])


class FileMixin:
    def write_to_file(self, data: dict, file_name) -> None:
        """Write the data to the specified file. """
        raise NotImplementedError

    def read_from_file(self, file_name) -> None:
        """Read the data from the specified file. """
        raise NotImplementedError


class CSVSerializer(FileMixin):
    def write_to_file(self, data: dict, file_name) -> None:
        """Write data to file. """
        with open(file_name, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['type', 'total', 'healthy'])
            for tree_type, info in data.items():
                writer.writerow([tree_type, info['total'], info['healthy']])

    def read_from_file(self, file_name) -> 'Forest':
        """Read data from file. """
        forests = dict()
        with open(file_name, "r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                forests[row['type']] = {"total": int(row['total']), "healthy": int(row['healthy'])}
        return Forest(forests)


class PickleSerializer(FileMixin):
    def write_to_file(self, data: dict, file_name) -> None:
        """Write data to file. """
        with open(file_name, "wb") as file:
            pickle.dump(data, file)

    def read_from_file(self, file_name) -> 'Forest':
        """Read data from file. """
        with open(file_name, "rb") as file:
            return Forest(pickle.load(file))


def is_command(value: str) -> int:
    """Checks the value to be between 0 and 11. """
    while True:
        try:
            value = int(value)
            if 0 < value < 11:
                return value
            value = input("Value should be between 0 and 11, input value: ")
        except ValueError:
            value = input("Invalid input, please enter a valid value: ")


def menu() -> None:
    """Menu for user input. """
    print("\n1: Writing to a file using CSV")
    print("2: Reading from a file using CSV")
    print("3: Writing to a file using pickle")
    print("4: Reading from a file using pickle")
    print("5: Display the total number of trees in the control area")
    print("6: Display the total number of healthy trees")
    print("7: Display the relative abundance (%) of diseased trees")
    print("8: Display the relative abundance (%) different species, including patients (%) for each species")
    print("9: Display the information about the type of tree entered from the keyboard")
    print("10: Exit\n")


def main() -> None:
    data = {
        "Pine": {"total": 500, "healthy": 100},
        "Ash": {"total": 110, "healthy": 100},
        "Oak": {"total": 50, "healthy": 10}
    }
    forest = Forest(data)
    csv_serializer = CSVSerializer()
    pickle_serializer = PickleSerializer()
    while True:
        menu()
        command = is_command(input("Enter value: "))
        if command == 1:
            csv_serializer.write_to_file(data, "forest.csv")
        if command == 2:
            forest = csv_serializer.read_from_file("forest.csv")
        if command == 3:
            pickle_serializer.write_to_file(data, "forest.txt")
        if command == 4:
            forest = pickle_serializer.read_from_file("forest.txt")
        if command == 5:
            print(forest.total_trees_count())
        if command == 6:
            print(forest.total_healthy_trees_count())
        if command == 7:
            print(forest.relative_diseased_percent())
        if command == 8:
            print(forest.relative_diseased_percent_by_type())
        if command == 9:
            print(forest.get_tree(input("\nEnter the tree: ")))
        if command == 10:
            break
