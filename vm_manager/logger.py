import sys

import settings


def log_info(*args):
    if settings.verbose:
        if settings.debug is not True:
            print("LOG: ", end="")
        print(*args)


def log_error(*args):
    print("ERR: ", end="", file=sys.stderr)
    print(*args, file=sys.stderr)


def log_fatal(*args):
    print("FATAL: ", end="")
    print(*args)
    print("Terminated")
    exit(1)
