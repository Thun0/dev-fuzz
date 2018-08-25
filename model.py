from project import Project
from corpus.corpus import Corpus
from pathlib import Path
from android import utils
import threading
import settings
from fuzzer import Fuzzer
from corpus.corpus import Corpus
import random


class Model:

    def __init__(self):
        random.seed()
        self.saved = False
        self.log = ''
        self.project = None
        self.view = None
        self.corpus = None
        self.devices = []
        self.fuzzers = []
        self.threads = []
        self.get_devices()

    def install_busybox(self):
        if len(self.devices) is not 0:
            self.view.log('Instaluję busybox...\n')
            for d in self.devices:
                if d.rooted:
                    d.install_busybox()
            self.view.log('Busybox zainstalowany\n')

    def new_project(self, filepath, name):
        self.project = Project(name=name)
        self.project.create(filepath)
        self.view.init()
        threading.Thread(target=self.install_busybox).start()
        self.corpus = Corpus(self.project.corpuspath)

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
        threading.Thread(target=self.install_busybox).start()

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

    def start_run(self, chosen_devices, methods):
        print(methods)
        #port = settings.config['devices_start_port']
        port = 1337
        self.view.log('Instaluję agenta na urządzeniach ({})...\n'.format(len(chosen_devices)))
        for idx in chosen_devices:
            self.devices[idx].device.push(settings.config['agent_path'], '/data/local/tmp/agent', 0o755)
            self.fuzzers.append(Fuzzer(self.devices[idx], port, self.project.devpath, self.corpus, methods))
            port += 1
        for f in self.fuzzers:
            t = threading.Thread(target=f.run, daemon=True)
            self.threads.append(t)
            t.start()
        self.view.log('Rozpoczęto testowanie!\n')
