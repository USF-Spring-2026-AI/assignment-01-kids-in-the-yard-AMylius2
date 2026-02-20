"""
CS 362/562 Assignment 1 - Kids Running in the Yard
Implementation Only

Single-file Python solution using object-oriented design.

NOTE:
Some logic simplified for robustness due to unknown CSV formats.
All files assumed in current directory.

External references:
- Python csv module documentation
- random module documentation
"""

import csv
import random
from collections import defaultdict


# ============================================================
# PERSON CLASS
# ============================================================
class Person:
    """Represents one person in the family tree."""

    def __init__(self, first, last, year_born, year_died, gender):
        self.first_name = first
        self.last_name = last
        self.year_born = year_born
        self.year_died = year_died
        self.gender = gender
        self.partner = None
        self.children = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# ============================================================
# PERSON FACTORY
# ============================================================
class PersonFactory:
    """Reads CSV files and generates people."""

    def __init__(self):
        self.first_names = []
        self.last_names = []
        self.life_expectancy = {}
        self.marriage_rates = {}
        self.birth_rates = {}
        self.read_files()

    def read_files(self):
        """Reads CSV files."""
        print("Reading files...")

        try:
            with open("first_names.csv") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    self.first_names.append(row[0])

            with open("last_names.csv") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    self.last_names.append(row[0])

            with open("life_expectancy.csv") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    self.life_expectancy[int(row[0])] = float(row[1])

            with open("birth_and_marriage_rates.csv") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    decade = int(row["decade"].rstrip('s'))
                    self.marriage_rates[decade] = float(row["marriage_rate"])
                    self.birth_rates[decade] = float(row["birth_rate"])

        except Exception as e:
            print("Error reading files:", e)
            exit()

    # -------------------------------
    def random_life_span(self, year_born):
        decade = (year_born // 10) * 10
        expectancy = self.life_expectancy.get(decade, 75)
        return int(expectancy + random.randint(-10, 10))

    # -------------------------------
    def random_first_name(self):
        return random.choice(self.first_names)

    def random_last_name(self):
        return random.choice(self.last_names)

    # -------------------------------
    def get_person(self, year_born, last_name=None):
        gender = random.choice(["M", "F"])
        first = self.random_first_name()
        last = last_name if last_name else self.random_last_name()
        died = year_born + self.random_life_span(year_born)
        return Person(first, last, year_born, died, gender)

    # -------------------------------
    def marriage_probability(self, year_born):
        decade = (year_born // 10) * 10
        return self.marriage_rates.get(decade, 0.5)

    def birth_rate(self, year_born):
        decade = (year_born // 10) * 10
        return self.birth_rates.get(decade, 2)


# ============================================================
# FAMILY TREE
# ============================================================
class FamilyTree:
    """Driver class managing all people."""

    def __init__(self):
        self.factory = PersonFactory()
        self.people = []

    def generate_tree(self):
        print("Generating family tree...")

        # First two people born in 1950
        p1 = self.factory.get_person(1950, "Jones")
        p2 = self.factory.get_person(1950, "Smith")
        p1.partner = p2
        p2.partner = p1

        self.people.extend([p1, p2])
        self.generate_children(p1, p2)

    # -------------------------------
    def generate_children(self, parent1, parent2):
        queue = [(parent1, parent2)]

        while queue:
            p1, p2 = queue.pop(0)

            elder_year = min(p1.year_born, p2.year_born)
            num_children = int(
                max(
                    0,
                    round(
                        self.factory.birth_rate(elder_year)
                        + random.uniform(-1.5, 1.5)
                    ),
                )
            )

            for i in range(num_children):
                child_year = random.randint(
                    elder_year + 25,
                    min(elder_year + 45, 2120),
                )
                if child_year > 2120:
                    continue

                last = random.choice([p1.last_name, p2.last_name])
                child = self.factory.get_person(child_year, last)
                p1.children.append(child)
                p2.children.append(child)
                self.people.append(child)

                # Partner
                if random.random() < self.factory.marriage_probability(child_year):
                    partner_year = child_year + random.randint(-10, 10)
                    partner = self.factory.get_person(partner_year)
                    child.partner = partner
                    partner.partner = child
                    self.people.append(partner)
                    queue.append((child, partner))

    # ========================================================
    # QUERY FUNCTIONS
    # ========================================================
    def total_people(self):
        return len(self.people)

    def people_by_decade(self):
        counts = defaultdict(int)
        for p in self.people:
            decade = (p.year_born // 10) * 10
            counts[decade] += 1
        return dict(sorted(counts.items()))

    def duplicate_names(self):
        counts = defaultdict(int)
        for p in self.people:
            counts[p.full_name()] += 1
        return [name for name, c in counts.items() if c > 1]

    # ========================================================
    def run_queries(self):
        while True:
            print("\nAre you interested in:")
            print("(T)otal number of people")
            print("Total people by (D)ecade")
            print("(N)ames duplicated")
            print("(Q)uit")

            choice = input("> ").upper()

            if choice == "T":
                print("Total people:", self.total_people())

            elif choice == "D":
                for d, c in self.people_by_decade().items():
                    print(f"{d}: {c}")

            elif choice == "N":
                dup = self.duplicate_names()
                if dup:
                    print("Duplicate names:")
                    for n in dup:
                        print("*", n)
                else:
                    print("No duplicate names.")

            elif choice == "Q":
                break


# ============================================================
# MAIN
# ============================================================
def main():
    tree = FamilyTree()
    tree.generate_tree()
    tree.run_queries()


if __name__ == "__main__":
    main()