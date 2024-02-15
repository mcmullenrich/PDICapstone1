"""PDI Budget Module

A module to greet your PDI Coach

$ python -m pydoc budget

The file can be run with:

$ python -m budget

or

$ python budget.py
"""
import json
import os
import sys

def load_budget(filename: str) -> dict:
    return json.load(open(filename))

def save_budget(budget: dict, filename: str) -> None:
    json.dump(budget, open(filename, "w"))

def print_budget(budget: dict) -> None:
    print(f"Budget Name: {budget['name']}; Budget Description: {budget['description']}")
    for entry in budget["entries"]:
        print(entry)

def enter_item(budget: dict):
    entry_type = input("What type of item is it? Income or expense? ")
    entry_category = input("What category is it? ")
    entry_amount = input("How much was the item? ")
    budget["entries"].append(entry_type, entry_category, entry_amount)

def create_budget():
    name = input("Enter a name for the budget. ")
    description = input(f"Enter a description for the {name} budget. ")
    result = {"name": name, "description": description, "entries": []}
    return result

def disply_menu() -> str:
    command = input("""

Welcome to the PDI Budget Module

1. Load Budget (L)

2. Save Budget (S)

3. Create Budget (C)

4. Enter Item (E)

5. Print Budget (P)

6. Quit (Q)
                     """)
    return command

def main() -> int:
    os.system('cls')
    while True:
        command = disply_menu()
        print(command)
        if command.lower().startswith("c"):
            cmd = command
            budget = create_budget()
        if command.lower().startswith("e"):
            # flesh this out. what are we entering here?
            try:
                enter_item(budget)
            except ValueError:
                print("Please include an entry type.")
                continue
        if command.lower().startswith("q"):
            break
        if command.lower().startswith("p"):
            try:
                print_budget(budget)
            except UnboundLocalError:
                print("Make a budget first!")
                continue
        if command.lower().startswith("l"):
            try:
                cmd, filename = command.split(maxsplit=1)
                budget = load_budget(filename)
            except Exception as error:
                print(error)
                continue
        if command.lower().startswith("s"):
            try:
                cmd, filename = command.split(maxsplit=1)
                budget = save_budget(budget, filename)
            except Exception as error:
                print(error)
                continue
    print("Bye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())