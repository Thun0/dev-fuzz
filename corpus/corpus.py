from os import listdir
import settings
import random


class Corpus:

    inputs = []

    def __init__(self, dir_path=None):
        if dir_path is None:
            dir_path = settings.config["corpus"]["dir_path"]
        for file in listdir(dir_path):
            self.inputs.append(file)

    def add_case(self, case):
        self.inputs.append(case)
        filename = self.generate_name()
        with open(filename) as f:
            f.write(case)

    def generate_name(self):
        return "sample_"+str(len(self.inputs))

    def get_random_input(self):
        idx = random.randint(0, len(self.inputs))
        return self.inputs[idx]
