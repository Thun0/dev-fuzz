import random
import copy
from settings import config


# TODO: Create params in mutator and create default mutator from config. Multiple mutators available.
class Mutator:
    """
    Set of mutator functions
    """

    def __init__(self, data):
        self.data = bytearray(copy.copy(data).encode())

    def randomize_bytes(self):
        """
        Randomizes bytes in data. Maximum bytes to change is specified in settings.
        """
        max_bytes_to_change = int(len(self.data)*config["mutator"]["max_mutated_bytes"])
        if max_bytes_to_change == 0:
            max_bytes_to_change = 1
        bytes_to_change = random.randint(1, max_bytes_to_change)
        self.randomize_n_bytes(bytes_to_change)

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
        for b in bytes_list:
            self.data.append(b)

    def insert_bytes(self, idx, bytes_list):
        bytes_list.reverse()
        for b in bytes_list:
            self.data.insert(idx, b)

    def flip_bits(self):
        max_bits_to_flip = int(8*len(self.data)*config["mutator"]["max_flipped_bits"])
        if max_bits_to_flip == 0:
            max_bits_to_flip = 1
        self.flip_n_bits(random.randint(1, max_bits_to_flip))

    def flip_n_bits(self, n):
        print('flipping {} bits'.format(n))
        for _ in range(n):
            byte = random.randint(0, len(self.data)-1)
            bit = random.randint(0, 7)
            self.data[byte] = self.data[byte] ^ (1 << bit)
