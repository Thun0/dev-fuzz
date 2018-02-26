from os import listdir
import settings

class Corpus:

    inputs = []

    def __init__(self, dir_path=None):
        if dir_path is None:
            dir_path = settings.config["corpus"]["dir_path"]
        for file in listdir(dir_path):
            self.inputs.append(file.read())

    def add_input(self, input):
        self.inputs.append(input)
        filename = self.generate_name()
        with open(filename) as f:
            f.write(input)

    def generate_name(self):
        return "sample_"+str(len(self.inputs))
