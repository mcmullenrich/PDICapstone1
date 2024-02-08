"""PDI Coach Greeting Module

A module to greet your PDI Coach

$ python -m pydoc utility

The file can be run with:

$ python -m utility

or

$ python utility.py
"""

import sys
from argparse import ArgumentParser

def main() -> int:
    """The main function called for The PDI Coach Greeting Module."""

    parser = ArgumentParser(description="PDI Coach Greeting Module")
    
    parser.add_argument('name', type=str, help='The name of the PDI Coach')

    parser.add_argument('-g', '--greeting', type=str, help='Custom greeting message', default='Hello')

    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    args = parser.parse_args()

    greeting = f'{args.greeting}, {args.name}!'

    if args.verbose:
        print("Verbose mode enabled. Enjoy your detailed execution info!")
        print(f'{greeting} Thank you for teaching me about this module!')
    else:
        print(greeting)


    return 0

if __name__ == "__main__":
    sys.exit(main())