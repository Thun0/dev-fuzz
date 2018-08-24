from project import Project
from corpus.corpus import Corpus
from pathlib import Path
from android import utils


class Model:

    def __init__(self):
        self.saved = False
        self.log = ''
        self.project = None
        self.view = None
        self.corpus = None
        self.devices = []
        self.get_devices()

    def new_project(self, filepath, name):
        self.project = Project(name=name)
        self.project.create(filepath)
        print('Stworzylem')
        print(self.project.name)
        print(self.project.corpuspath)

    def load_project(self, filepath):
        self.project = Project()
        self.project.load(filepath)
        if self.project.corpuspath[0] is not '/':
            p = Path().absolute().parents[0]
            p /= Path(self.project.corpuspath)
            self.corpus = Corpus(p)
        else:
            self.corpus = Corpus(self.project.corpuspath)
        self.view.init()

    def save_project(self, filepath):
        self.project.filepath = filepath
        self.project.save()

    def get_devices(self):
        self.devices = utils.get_devices()
        return self.devices

    def list_dev_paths(self):
        char_devs = []
        for d in self.devices:
            char_devs.extend(d.get_char_devices())
        return char_devs

    def start_run(self):
        pass
