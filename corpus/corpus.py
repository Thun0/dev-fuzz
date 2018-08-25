from os import listdir
import random


class Corpus:

    ioctl_inputs = []
    write_inputs = []
    mmap_inputs = []

    def __init__(self, dirpath):
        self.dirpath = dirpath
        self.reload()

    def reload(self):
        self.ioctl_inputs = []
        self.write_inputs = []
        self.mmap_inputs = []

        for file in listdir('{}/{}'.format(self.dirpath,'ioctl')):
            with open(file, mode='rb') as f:
                self.ioctl_inputs.append(f.read())
        print('Zaladowano {} plikow do korpusu (ioctl)'.format(len(self.ioctl_inputs)))

        for file in listdir('{}/{}'.format(self.dirpath,'write')):
            with open(file, mode='rb') as f:
                self.write_inputs.append(f.read())
        print('Zaladowano {} plikow do korpusu (write)'.format(len(self.write_inputs)))

        for file in listdir('{}/{}'.format(self.dirpath,'mmap')):
            with open(file, mode='rb') as f:
                self.mmap_inputs.append(f.read())
        print('Zaladowano {} plikow do korpusu (mmap)'.format(len(self.mmap_inputs)))

    def add_case(self, case, method):
        if method is 'ioctl':
            self.ioctl_inputs.append(case)
        if method is 'write':
            self.write_inputs.append(case)
        if method is 'mmap':
            self.mmap_inputs.append(case)
        filename = self.generate_name(method)
        with open('{}/{}/{}'.format(self.dirpath, method, filename), mode='wb') as f:
            f.write(case)

    def generate_name(self, method):
        if method is 'ioctl':
            return "sample_"+str(len(self.ioctl_inputs))
        if method is 'write':
            return "sample_"+str(len(self.write_inputs))
        if method is 'mmap':
            return "sample_"+str(len(self.mmap_inputs))

    def get_random_input(self, method):
        if method is 'ioctl':
            idx = random.randint(0, len(self.ioctl_inputs))
            return self.ioctl_inputs[idx].split('\n')
        if method is 'write':
            idx = random.randint(0, len(self.write_inputs))
            return self.write_inputs[idx].split('\n')
        if method is 'mmap':
            idx = random.randint(0, len(self.mmap_inputs))
            return self.mmap_inputs[idx].split('\n')
