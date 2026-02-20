import random
from PersonFactory import PersonFactory
from collections import Counter
from Person import Person

def main():
    """main loop for handling input and giving output"""
    ft = FamilyTree()
    ft.generate_tree()
    ft.tree_to_dict()
    stop = False

    while not stop:
        print("Are you interested in:\n (T)otal number of people in the tree\nTotal number of people in the tree by (D)ecade\n (N)ames duplicated\n (E)xiting")
        response = input("> ")

        if response == "T":
            print("The tree contains", len(ft.list), "people total")

        elif response == "D":
            for i in range(1940, 2120, 10):
                if i in ft.dict:
                    print(str(i) + ": " + str(ft.dict[i].__len__()))

        elif response == "N":
            names = ft.get_duplicates()
            print("There are", names.__len__(), "duplicate names in the tree:")
            for name in names:
                print(name)

        elif response == "E":
            stop = True

        else:
            print("Response not understood, try again.")

    print("Have a nice day!")


class FamilyTree:

    def __init__(self):
        """initializes family tree object"""
        self.pf = PersonFactory()
        self.root_person_one = self.pf.get_person(1950)
        self.root_person_two = self.pf.get_person(1950)
        self.dict = {}
        self.list = []
        self.count = 0

    def get_duplicates(self):
        """method which gets a list of names that occur multiple times and returns it"""
        counts = Counter(self.list)
        duplicates = [item for item, count in counts.items() if count > 1]
        return duplicates

    def generate_tree(self):
        """helper method which converts the trees starting with the first two people into a dictionary
        with decades and lists of people"""

        print("generating family tree...")
        self.generate_tree_person(self.root_person_one)
        self.generate_tree_person(self.root_person_two)
    def generate_tree_person(self, current_person, from_partner=False):
        """recursively generates a tree from a given person"""

        # generate children and add them to list of children, making sure they have the proper last name and birth year
        num_children = self.pf.num_children(current_person.get_decade())
        for i in range(num_children):
            born = current_person.get_born() + random.randint(25, 45)
            if born <= 2120:
                current_person.add_child(self.pf.get_person(born, current_person.get_last_name()))

        # for any children in the list of children, call this method recursively on them
        for child in current_person.get_children():
            self.generate_tree_person(child)

        # if the current person has a partner, call this method recursively on them
        if current_person.has_partner():
            if not from_partner:
                self.generate_tree_person(current_person.get_partner(), True)

    def tree_to_dict(self):
        """helper method which converts the trees starting with the first two people into a dictionary
        with decades and lists of people"""

        self.dict_from_tree(self.root_person_one)
        self.dict_from_tree(self.root_person_two)

    def dict_from_tree(self, current_person, from_partner=False):
        """recursively write to dictionary with decades as keys and lists of people as values"""

        # add current person to the list stored by their decade's key (and add their name to a list of names)
        decade = current_person.get_decade()
        if not (decade in self.dict):
            self.dict[decade] = []
        self.dict[decade].append(current_person)
        self.list.append(current_person.get_name())

        # call method recursively on children
        for child in current_person.get_children():
            self.dict_from_tree(child)

        # call method recursively on partner
        if current_person.has_partner() :
            if not from_partner:
                self.dict_from_tree(current_person.get_partner(), True)


main()