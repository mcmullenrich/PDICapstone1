"""
"""
import json
import sys

def load_budget(filename: str) -> dict:
    return json.load(open(filename))

def save_budget(budget: dict, filename: str) -> None:
    json.dump(budget, open(filename, "w"))

def print_budget(budget: dict) -> None:
    print(f"Budget Name: {budget['name']}; Budget Description: {budget['description']}")
    for entry in budget["entries"]:
        print(entry)

def enter_item(budget: dict, entry_type: str):
    entry = input("Enter a budget item. ")
    budget["entries"].append(entry)
    print(f"Comes from enter_item: {entry_type}")

def create_budget(name: str):
    description = input("Enter a description. ")
    print(f"Hello, I am a budget named {name}.")
    result = {"name": name, "description": description, "entries": []}
    return result

def disply_menu() -> str:
    command = input("Type a command. ")
    return command

def main() -> int:
    while True:
        command = disply_menu()
        print(command)
        if command.lower().startswith("create"):
            cmd, name = command.split(maxsplit=1)
            budget = create_budget(name)
            print(budget)
        if command.lower().startswith("enter"):
            # flesh this out. what are we entering here?
            try:
                cmd, entry_type = command.split(maxsplit=1)
                enter_item(budget, entry_type)
            except ValueError:
                print("Please include an entry type.")
                continue
        if command.lower().startswith("q"):
            break
        if command.lower().startswith("print"):
            try:
                print_budget(budget)
            except UnboundLocalError:
                print("Make a budget first!")
                continue
        if command.lower().startswith("load"):
            try:
                cmd, filename = command.split(maxsplit=1)
                budget = load_budget(filename)
            except Exception as error:
                print(error)
                continue
        if command.lower().startswith("save"):
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