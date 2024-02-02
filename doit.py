"""  Cool Module

This text shows up when the file is inspected with

$ python -m pydoc doit

The file can be run with:

$ python -m doit

or

$ python doit.py

"""

import sys

from argparse import ArgumentParser


def main() -> int:
    """The main function called for this cool module."""

    print("Hello world!")

    parser = ArgumentParser()

    # docs.python.org or pydoc argparse.ArgumentParser
    # parse the arguments command line
    # setup elements of the program based on the arguments
    # perform the computation
    # cleanup
    # exit

    return 0


if __name__ == "__main__":

    sys.exit(main())
