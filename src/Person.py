class Person:

    def __init__(self, born, died, first_name, last_name):
        """initializes person object"""
        self.born = born
        self.died = died
        self.first_name = first_name
        self.last_name = last_name
        self.partner = None
        self.children = []

    # minor getter, setter, and helper methods
    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def set_partner(self, partner):
        self.partner = partner

    def get_partner(self):
        return self.partner

    def has_partner(self):
        return self.partner is not None

    def get_born(self):
        return self.born

    def get_decade(self):
        return self.born - self.born % 10

    def get_died(self):
        return self.died

    def get_last_name(self):
        return self.last_name
    def get_name(self):
        return self.first_name + " " + self.last_name
