"""PDI Budget Module

Welcome to the PDI Budget Module! 

You can use this module to create a budget and track against it.

$ python -m pydoc budget

The file can be run with:

$ python -m budget

or

$ python budget.py
"""

from collections import namedtuple
from datetime import datetime
import json
import sys

Entry = namedtuple("Entry", "entry_type kind category date amount")

class Budget:
    def __init__(self, name: str, description: str, start_date: str, end_date: str) -> None:
        self.name = name
        self.description = description
        self.start_date = datetime.strptime(start_date, "%m/%d/%y").date()
        self.end_date = datetime.strptime(end_date, "%m/%d/%y").date()
        self.entries = []

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
    
    def add_entry(self, entry_type: str, kind: str, category: str, date: datetime.date, amount: float) -> None:
        self.entries.append(Entry(entry_type, kind, category, date, amount))
        print(f"Added {entry_type} {kind}: {category} on {date.strftime('%m/%d/%Y')} - ${amount: .2f}")

    def enter_item(self):
        entry_type = input("Is this a (b)udget entry or an (a)ctual entry? ")
        entry_type = "budget_entry" if entry_type.lower().startswith('b') else "actual_entry"
        entry_kind = input("What type of item is it? Income or expense? ")
        entry_category = input("What category is it? ")

        while True:
            entry_date = input("Enter the date of the item (MM/DD/YY): ")
            try:
                entry_date_obj = datetime.strptime(entry_date, "%m/%d/%y").date()
                if not self.start_date <= entry_date_obj <= self.end_date:
                    raise ValueError("Entry date is outside the budget period.")
                break
            except ValueError as error:
                print(f"Invalid date. {error}")

        while True:
            try:
                entry_amount = float(input("How much was the item? "))
                if entry_amount < 0:
                    raise ValueError("Amount must be positive.")
                break
            except ValueError as error:
                print(f"Invalid amount. Please try again. Error: {error}")
        self.add_entry(entry_type, entry_kind, entry_category, entry_date_obj, entry_amount)

    def save(self, filename: str) -> None:
        data_to_save = {
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.strftime("%m/%d/%y"),
            'end_date': self.end_date.strftime("%m/%d/%y"),
            'entries': [(e.entry_type, e.kind, e.category, e.date.strftime("%m/%d/%y"), e. amount) for e in self.entries]
        }
        try:
            with open(filename, "w") as file:
                json.dump(data_to_save, file)
            print(f"Budget '{self.name}' saved successfully to {filename}.")
        except Exception as error:
            print(f"Failed to save budget: {error}")

    def print(self) -> None:
        print(f"Budget Name: {self.name}")
        print(f"Budget Description: {self.description}")
        for entry in self.entries:
            print(f"{entry.entry_type.title()}: {entry.kind}, {entry.category}, {entry.amount}")

    def generate_report(self):
        print("\nBudget vs. Actual Report:")
        print(f"{'Category':<20} {'Budgeted':>10} {'Actual':>10} {'Variance':>10}")

        category_totals = {}
        for entry in self.entries:
            if entry.category not in category_totals:
                category_totals[entry.category] = {'budgeted': 0, 'actual': 0}
            if entry.entry_type == 'budget_entry':
                category_totals[entry.category]['budgeted'] += entry.amount
            else:
                category_totals[entry.category]['actual'] += entry.amount

        for category, totals in category_totals.items():
            budgeted = totals['budgeted']
            actual = totals['actual']
            variance = actual - budgeted
            print(f"{category:<20} {budgeted:>10,.2f} {actual:>10,.2f} {variance:>10,.2f}")

        print("\n* A positive variance means actual spending/revenue was higher than budgeted.")
        
def display_menu() -> str:
    command = input("""

Welcome to the PDI Budget Module

1. (L)oad Budget - Load an existing budget from a file.

2. (S)ave Budget - Save the current budget to a file.

3. (C)reate Budget - Create a new budget.

4. (E)nter Item - Add a new budget or actual item.

5. (P)rint Budget - Display the current budget.
                    
6. (R)eport - Generate a budget vs. actual report.                  

7. (Q)uit - Exit the program.
                    
Enter a command. """)
    return command

def create_budget() -> Budget:
    name = input("Enter a name for the budget. ")
    description = input(f"Enter a description for the {name} budget. ")

    while True:
        start_date = input("Enter the start date of the budget (MM/DD/YY): ")
        end_date = input("Enter the end date of the budget (MM/DD/YY): ")

        try:
            start_date_obj = datetime.strptime(start_date, "%m/%d/%y").date()
            end_date_obj = datetime.strptime(end_date, "%m/%d/%y").date()

            if start_date_obj >= end_date_obj:
                raise ValueError("Start date must be before the end date.")
            break
        except ValueError as error:
            print(f"Invalid date(s). {error}")
    
    return Budget(name, description, start_date, end_date)

def load_budget(filename: str) -> Budget:
    with open(filename, 'r') as file:
        data = json.load(file)
    budget = Budget(data['name'], data['description'], data['start_date'], data['end_date'])
    budget.entries = [Entry(e[0], e[1], e[2], datetime.strptime(e[3], "%m/%d/%y").date(), e[4]) for e in data['entries']]
    return budget

def main() -> int:
    budget = None
    running = True

    def create_and_set_budget():
        nonlocal budget
        budget = create_budget()

    def quit():
        nonlocal running
        running = False
        print("Bye!")

    def load():
        nonlocal budget
        filename = input("Enter the filename to load: ")
        try:
            budget = load_budget(filename)
            print("Budget loaded successfully.")
        except Exception as error:
            print(f"Failed to load budget: {error}")

    def save():
        if budget:
            filename = input("Enter the filename to save: ")
            try:
                budget.save(filename)
                print("Budget saved successfully.")
            except Exception as error:
                print(f"Failed to save budget: {error}")
        else:
            print("No budget to save.")

    def print_budget():
        if budget:
            budget.print()
        else:
            print("No budget to print.")

    commands = {
        'c': create_and_set_budget,
        'e': lambda: budget and budget.enter_item(),
        'l': load,
        'p': print_budget,
        'q': quit,
        'r': lambda: budget and budget.generate_report(),
        's': save
    }
    
    while running:
        command = display_menu().lower()
        action = commands.get(command[0])
        if action:
            action()
        else:
            print("Invalid command. Please try again.")
    return 0


if __name__ == "__main__":
    sys.exit(main())