from Person import Person
import random


def randfloat():
    return float(random.randint(0, 1000) - 1) / 1000
class PersonFactory:
    def __init__(self):
        print("reading files...")

        # set up rank-to-probability list
        with open("../rank_to_probability.csv") as file:
                self.rtp = file.readlines()[0].rstrip().split(",")
                for i in range(self.rtp.__len__()):
                    self.rtp[i] = float(self.rtp[i])

        # set up dictionaries for first names by gender
        self.male_names = {}
        self.female_names = {}
        with open("../first_names.csv") as file:
            lines = file.readlines()
            for line in lines[1:]:

                data = line.rstrip().split(",")
                decade = int(data[0].rstrip('s'))
                gender = data[1]
                name = data[2]
                frequency = float(data[3])

                if gender == "male":
                    if not (decade in self.male_names):
                        self.male_names[decade] = []
                    self.male_names[decade].append([name, frequency])

                elif gender == "female":
                    if not (decade in self.female_names):
                        self.female_names[decade] = []
                    self.female_names[decade].append([name, frequency])

        self.gender_distribution = {}
        with open("../gender_name_probability.csv") as file:
            lines = file.readlines()
            male_prob = 0
            for line in lines[1:]:
                data = line.rstrip().split(",")
                decade = int(data[0].rstrip('s'))
                gender = data[1]
                probability = float(data[2])

                if gender == "male":
                    male_prob = probability
                elif gender == "female":
                    self.gender_distribution[decade] = [male_prob, probability]

        self.last_names = {}
        with open ("../last_names.csv") as file:
            lines = file.readlines()
            for line in lines[1:]:
                data = line.rstrip().split(",")
                decade = int(data[0].rstrip('s'))
                name = data[2]
                if not decade in self.last_names:
                    self.last_names[decade] = []
                self.last_names[decade].append(name)

        self.rates = {}
        with open ("../birth_and_marriage_rates.csv") as file:
            lines = file.readlines()
            for line in lines[1:]:
                data = line.rstrip().split(",")
                decade = int(data[0].rstrip('s'))
                birth = float(data[1])
                marriage = float(data[2])
                self.rates[decade] = [birth, marriage]

        self.life_expectancy = {}
        with open("../life_expectancy.csv") as file:
            lines = file.readlines()
            for line in lines[1:]:
                data = line.rstrip().split(",")
                year = int(data[0].rstrip('s'))
                self.life_expectancy[year] = float(data[1])

    def get_decade(self, year):
        return year - year % 10

    def num_children(self, decade):
        return random.randint(round(self.rates[decade][0]-1.5), round(self.rates[decade][0] + 1.5))

    def is_married(self, decade):
        return randfloat() < self.rates[decade][1]

    def choose_last_name(self, decade):
        # since the probabilities in the rank_to_probability.csv only add to 71.91%, the algorithm has been modified
        # so that .7191 is the highest value that can be rolled here
        threshold = float(random.randint(1, 7191) - 1) / 10000
        value = 0
        for i in range(30):
            value += self.rtp[i]
            if value >= threshold:
                return self.last_names[decade][i]

    def choose_first_name(self, decade):
        roll = randfloat()
        if roll < 0.5:
            name_dict = self.male_names
        else:
            name_dict = self.female_names

        threshold = randfloat()
        value = 0
        for item in name_dict[decade]:
            value += item[1]
            if value >= threshold:
                return item[0]

    def get_person(self, born, family_name="", partner=None):

        # calculate decade of birth and year of death
        decade = self.get_decade(born)
        died = int(born + self.life_expectancy[self.get_decade(born)] + random.randint(-10, 10))

        # choose first and last name if necessary
        if family_name != "":
            last_name = family_name
        else:
            last_name = self.choose_last_name(decade)

        first_name = self.choose_first_name(decade)

        # create the person with the info we've collected
        this_person = Person(born, died, first_name, last_name)

        # if this method not called with partner, try to generate one
        if partner is None:
            if self.is_married(decade):
                partner_birth = born + random.randint(-10, 10)
                if partner_birth < 1950:
                    partner_birth = 1950
                if partner_birth > 2120:
                    partner_birth = 2120
                partner = self.get_person(partner_birth, "", this_person)

        # set partner and return person
        this_person.set_partner(partner)
        return this_person
