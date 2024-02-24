"""PDI Budget Module

Welcome to the PDI Budget Module! 

You can use this module to create a budget and track against it.

$ python -m pydoc budget

The file can be run with:

$ python -m budget

or

$ python budget.py
"""

"""
TODO List for budget.py:
- Remove duplication of date parsing/validation logic
- Should Entry be a class instead of a namedtuple? If not now, what would make the answer yes?
- Add the ability to:
        - delete a budget
        - delete an entry
        - edit a budget
        - edit an entry
        - batch upload budget entries from excel file
        - batch upload actual entries from excel file
"""

from collections import namedtuple
from colorama import Fore, Style
from datetime import datetime
import json
import os
import platform
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
        print(f"{Fore.GREEN}Added {entry_type} {kind}: {category} on {date.strftime('%m/%d/%Y')} - ${amount: .2f}{Style.RESET_ALL}")

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
                    raise ValueError(f"{Fore.RED}Entry date is outside the budget period.{Style.RESET_ALL}")
                break
            except ValueError as error:
                print(f"{Fore.RED}Invalid date. {error}{Style.RESET_ALL}")

        while True:
            try:
                entry_amount = float(input("How much was the item? "))
                if entry_amount < 0:
                    raise ValueError(f"{Fore.RED}Amount must be positive.{Style.RESET_ALL}")
                break
            except ValueError as error:
                print(f"{Fore.RED}Invalid amount. Please try again. Error: {error}{Style.RESET_ALL}")
        self.add_entry(entry_type, entry_kind, entry_category, entry_date_obj, entry_amount)

    def save(self, filename: str) -> None:
        try:
            data_to_save = {
                'name': self.name,
                'description': self.description,
                'start_date': self.start_date.strftime("%m/%d/%y"),
                'end_date': self.end_date.strftime("%m/%d/%y"),
                'entries': [
                    (e.entry_type, e.kind, e.category, e.date.strftime("%m/%d/%y"), e.amount)
                    for e in self.entries
                ]
            }
            with open(filename, "w") as file:
                json.dump(data_to_save, file)
            print(f"{Fore.GREEN}Budget '{self.name}' saved successfully to {filename}.{Style.RESET_ALL}")
        except Exception as error:
            print(f"{Fore.RED}Failed to save budget: {error}{Style.RESET_ALL}")

    def print(self) -> None:
        print(f"Budget Name: {self.name}")
        print(f"Budget Description: {self.description}")
        for entry in self.entries:
            print(f"{entry.entry_type.title()}: {entry.kind}, {entry.category}, {entry.amount}")

    def generate_report(self):
        report_start = input("Enter the start date for the report (MM/DD/YY): ")
        report_end = input("Enter the end date for the report (MM/DD/YY): ")
        
        report_start_date = datetime.strptime(report_start, "%m/%d/%y").date()
        report_end_date = datetime.strptime(report_end, "%m/%d/%y").date()
        
        print("\nBudget vs. Actual Report:")
        print(f"Report Date Range: {report_start} to {report_end}")
        
        category_aggregates = {'Income': {}, 'Expense': {}}

        for entry in self.entries:
            if report_start_date <= entry.date <= report_end_date:
                entry_kind_normalized = "Income" if entry.kind.lower().startswith('i') else "Expense"
                kind_aggregates = category_aggregates[entry_kind_normalized]
                
                if entry.category not in kind_aggregates:
                    kind_aggregates[entry.category] = {'budgeted': 0, 'actual': 0}
                kind = 'budgeted' if entry.entry_type == 'budget_entry' else 'actual'
                kind_aggregates[entry.category][kind] += entry.amount

        for kind, categories in category_aggregates.items():
            kind_color = Fore.LIGHTGREEN_EX if kind == "Income" else Fore.LIGHTRED_EX
            print(f"\n{kind_color}{kind}:{Style.RESET_ALL}")
            print(f"{'Category':<20} {'Budgeted':>10} {'Actual':>10} {'Variance $':>10} {'Variance %':>10}")
            
            subtotal_budgeted = 0
            subtotal_actual = 0
            
            for category, amounts in categories.items():
                budgeted = amounts['budgeted']
                actual = amounts['actual']
                variance_dollar = actual - budgeted
                subtotal_budgeted += budgeted
                subtotal_actual += actual
                
                variance_color = Fore.GREEN if (variance_dollar >= 0 and kind == "Income") or (variance_dollar < 0 and kind == "Expense") else Fore.RED
                variance_percent = "-nm-"
                if budgeted > 0:
                    variance_percentage = (variance_dollar / budgeted) * 100
                    variance_percent = f"{variance_percentage:.2f}%"
                
                print(f"{category:<20} {budgeted:>10,.2f} {actual:>10,.2f} {variance_color}{variance_dollar:>10,.2f}{Style.RESET_ALL} {variance_color}{variance_percent:>10}{Style.RESET_ALL}")
            
            subtotal_variance = subtotal_actual - subtotal_budgeted
            subtotal_variance_color = Fore.GREEN if (subtotal_variance >= 0 and kind == "Income") or (subtotal_variance < 0 and kind == "Expense") else Fore.RED
            subtotal_variance_percent = "-nm-"
            if subtotal_budgeted > 0:
                subtotal_variance_percentage = (subtotal_variance / subtotal_budgeted) * 100
                subtotal_variance_percent = f"{subtotal_variance_percentage:.2f}%"
            
            print(f"{'Subtotal':<20} {subtotal_budgeted:>10,.2f} {subtotal_actual:>10,.2f} {subtotal_variance_color}{subtotal_variance:>10,.2f}{Style.RESET_ALL} {subtotal_variance_color}{subtotal_variance_percent:>10}{Style.RESET_ALL}")

        net_budgeted = sum(amounts['budgeted'] for amounts in category_aggregates['Income'].values()) - sum(amounts['budgeted'] for amounts in category_aggregates['Expense'].values())
        net_actual = sum(amounts['actual'] for amounts in category_aggregates['Income'].values()) - sum(amounts['actual'] for amounts in category_aggregates['Expense'].values())
        net_variance = net_actual - net_budgeted
        net_variance_color = Fore.GREEN if net_variance >= 0 else Fore.RED
        net_variance_percent = "-nm-"
        if net_budgeted > 0:
            net_variance_percentage = (net_variance / net_budgeted) * 100
            net_variance_percent = f"{net_variance_percentage:.2f}%"
        
        print("\nSummary:")
        print(f"{'Net Budgeted':<20} ${net_budgeted:>10,.2f}")
        print(f"{'Net Actual':<20} ${net_actual:>10,.2f}")
        print(f"{net_variance_color}{'Net Variance $':<20} ${net_variance:>10,.2f}{Style.RESET_ALL}")
        print(f"{net_variance_color}{'Net Variance %':<20} {net_variance_percent}{Style.RESET_ALL}")
        print("\n* A positive Net means total income exceeds total expenses within the specified period.")
        
def display_menu() -> str:
    command = input("""

Welcome to the PDI Budget Module

(L)oad Budget - Load an existing budget from a file.

(S)ave Budget - Save the current budget to a file.

(C)reate Budget - Create a new budget.

(E)nter Item - Add a new budget or actual item.

(P)rint Budget - Display the current budget.
                    
(R)eport - Generate a budget vs. actual report.                  

(W)ipe Screen - Clear the console screen.
                    
(H)elp - Display help/documentation.
                    
(Q)uit - Exit the program.
                    
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
                raise ValueError(f"{Fore.RED}Start date must be before the end date.{Style.RESET_ALL}")
            break
        except ValueError as error:
            print(f"{Fore.RED}Invalid date(s). {error}{Style.RESET_ALL}")
    
    return Budget(name, description, start_date, end_date)

def load_budget(filename: str) -> Budget:
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        budget = Budget(data['name'], data['description'], data['start_date'], data['end_date'])
        budget.entries = [Entry(e[0], e[1], e[2], datetime.strptime(e[3], "%m/%d/%y").date(), e[4]) for e in data['entries']]
        print(f"{Fore.GREEN}Budget '{budget.name}' loaded successfully from {filename}.{Style.RESET_ALL}")
        return budget
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The file '{filename}' was not found.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Failed to decode JSON from '{filename}'. Please check the file format.{Style.RESET_ALL}")
    except Exception as error:
        print(f"{Fore.RED}Failed to load budget due to an unexpected error: {error}{Style.RESET_ALL}")

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
            budget.save()
        else:
            print(f"{Fore.RED}No budget to save.{Style.RESET_ALL}")

    def print_budget():
        if budget:
            budget.print()
        else:
            print("No budget to print.")

    def wipe_screen():
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def display_help():
        print(f"""
    {Fore.BLUE}Help:{Style.RESET_ALL}
    - (L)oad Budget: Load a budget from a specified file. Use the 'l' command followed by the file path.
    - (S)ave Budget: Save the current budget to a file. Use the 's' command followed by the desired file path for saving.
    - (C)reate Budget: Start a new budget with a name, description, and date range. Follow the prompts after using the 'c' command.
    - (E)nter Item: Add a new budget or actual income/expense item. Follow the prompts after using the 'e' command.
    - (P)rint Budget: Display the current state of your budget with all entries listed. Simply use the 'p' command.
    - (R)eport: Generate a report comparing budgeted and actual amounts for a specified period. Use the 'r' command and follow the prompts for date range.
    - (W)ipe Screen: Clear the console screen to reduce clutter. Use the 'w' command.
    - (H)elp: Display this help message for information on how to use the application. Use the 'h' command.
    - (Q)uit: Exit the application. Use the 'q' command when you're done.
    """)

    commands = {
        'c': create_and_set_budget,
        'e': lambda: budget and budget.enter_item(),
        'h': display_help,
        'l': load,
        'p': print_budget,
        'q': quit,
        'r': lambda: budget and budget.generate_report(),
        's': save,
        'w': wipe_screen
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