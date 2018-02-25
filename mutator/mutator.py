import random
from settings import config


# TODO: Create params in mutator and create default mutator from config. Multiple mutators available.
class Mutator:
    """
    Set of mutator functions
    """

    def __init__(self, data):
        self.data = data.copy()

    def randomize_bytes(self):
        """
        Randomizes bytes in data. Maximum bytes to change is specified in settings.
        """
        max_bytes_to_change = int(len(self.data)*config["mutator"]["max_mutated_bytes"])
        if max_bytes_to_change == 0:
            max_bytes_to_change = 1
        bytes_to_change = random.randint(1, max_bytes_to_change)
        Mutator.randomize_n_bytes(self.data, bytes_to_change)

    def randomize_n_bytes(self, n):
        """
        Randomizes n bytes in data.
        :param n: number of bytes to randomize
        """
        for _ in range(n):
            idx = random.randint(0, len(self.data) - 1)
            self.data[idx] = random.randint(0, 255)

    def remove_n_bytes(self, n):
        del self.data[-n:]

    def remove_n_bytes_at(self, idx, n):
        del self.data[idx:idx+n]

    def append_n_random_bytes(self, n):
        for _ in range(n):
            self.data.append(random.randint(0, 255))

    def append_bytes(self, bytes_list):
        self.data.extend(bytes_list)

    def insert_bytes(self, idx, bytes_list):
        bytes_list.reverse()
        for b in bytes_list:
            self.data.insert(idx, b)
