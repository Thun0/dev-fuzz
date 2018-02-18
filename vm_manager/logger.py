import sys

from settings import config


def log_info(*args):
    if config["verbose"]:
        if config["debug"] is not True:
            print("LOG: ", end="")
        print(*args)


def log_error(*args):
    print("ERR: ", end="", file=sys.stderr)
    print(*args, file=sys.stderr)


def log_fatal(*args):
    print("FATAL: ", end="")
    print(*args)
    print("Terminated")
    exit(-1)
