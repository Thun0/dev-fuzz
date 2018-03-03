import sys

from settings import config

class Logger:

    # TODO: push logs to file

    def __init__(self, file=sys.stdout):
        self.file = file

    def i(self, *args):
        if config["verbose"]:
            if config["debug"] is not True:
                print("LOG: ", end="")
            print(*args)


    def e(self, *args):
        print("ERR: ", end="", file=sys.stderr)
        print(*args, file=sys.stderr)


    def f(self, *args):
        print("FATAL: ", end="")
        print(*args)
        print("Terminated")
        exit(-1)
