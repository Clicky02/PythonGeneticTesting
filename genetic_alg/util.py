from contextlib import contextmanager
import os
import sys


@contextmanager
def suppressPrint():
    with open(os.devnull, "w") as devNull:
        orig = sys.stdout
        sys.stdout = devNull
        try:
            yield
        finally:
            sys.stdout = orig
