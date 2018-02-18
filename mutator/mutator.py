import random
from settings import config


# TODO: Create params in mutator and create default mutator from config. Multiple mutators available.
class Mutator:
    """
    Set of mutator functions
    """

    @staticmethod
    def randomize_bytes(data):
        """
        Randomizes bytes in data. Maximum bytes to change is specified in settings.
        :param data: data to mutate
        """
        max_bytes_to_change = int(len(data)*config["mutator"]["max_mutated_bytes"])
        if max_bytes_to_change == 0:
            max_bytes_to_change = 1
        bytes_to_change = random.randint(1, max_bytes_to_change)
        Mutator.randomize_n_bytes(data, bytes_to_change)

    @staticmethod
    def randomize_n_bytes(data, n):
        """
        Randomizes n bytes in data.
        :param data: data to mutate
        :param n: number of bytes to randomize
        """
        for _ in range(n):
            idx = random.randint(0, len(data) - 1)
            data[idx] = random.randint(0, 255)
