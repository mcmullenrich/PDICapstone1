"""PDI Budget Module

A module to greet your PDI Coach

$ python -m pydoc budget

The file can be run with:

$ python -m budget

or

$ python budget.py
"""
from collections import namedtuple
import json
import os
import sys

Entry = namedtuple("Entry", "kind category amount")

class Budget:
    def __init__(self, name: str, description: str) -> None:
        """
        """
        self.name = name
        self.description = description
        self.entries = []

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
    
    def save(self, filename: str) -> None:
        """Saves the budget as a json document with a filename
        """
        json.dump(self.__dict__, open(filename, "w"))

def load_budget(filename: str) -> dict:
    budget = json.load(open(filename))
    entries = []
    for raw in budget["entries"]:
        entries.append(Entry(*raw))
    budget["entries"] = entries
    return budget

def save_budget(budget: dict, filename: str) -> None:
    json.dump(budget, open(filename, "w"))

def print_budget(budget: dict) -> None:
    print(f"Budget Name: {budget['name']}; Budget Description: {budget['description']}")
    for entry in budget["entries"]:
        print(entry)

def enter_item(budget: Budget):
    entry_kind = input("What type of item is it? Income or expense? ")
    entry_category = input("What category is it? ")
    entry_amount = float(input("How much was the item? "))
    budget.entries.append(Entry(entry_kind, entry_category, entry_amount))

def create_budget() -> Budget:
    name = input("Enter a name for the budget. ")
    description = input(f"Enter a description for the {name} budget. ")
    #result = {"name": name, "description": description, "entries": []}
    result = Budget(name, description)
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
            except ValueError as error:
                print(f"An error occurred while entering budget. {error}")
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
                save_budget(budget, filename)
            except Exception as error:
                print(error)
                continue
    print("Bye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())