from project import Project


class Model:

    def __init__(self):
        self.saved = False
        self.log = ''
        self.project = None
        self.view = None

    def load_project(self, filepath):
        self.project = Project()
        self.project.load(filepath)
        self.view.init()

    def save_project(self, filepath):
        pass

    def list_dev_paths(self):
        pass
