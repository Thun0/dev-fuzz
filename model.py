from project import Project
from corpus.corpus import Corpus
from pathlib import Path


class Model:

    def __init__(self):
        self.saved = False
        self.log = ''
        self.project = None
        self.view = None
        self.corpus = None

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

    def list_dev_paths(self):
        pass
