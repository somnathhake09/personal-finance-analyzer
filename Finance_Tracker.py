
import json
from pathlib import Path

DATA_FILE = Path("transactions.json")

class Transaction:
    """Represents a single financial transaction."""

    count = 0

    def __init__(self, description, amount, category):
        self.description = description
        self.amount = amount
        self.category = category
        self.spend_type = self.classify()
        Transaction.count += 1

    def classify(self):
        """Returns Essential, Discretionary, or Unknown based on the category."""
        if self.category in ("Food", "Rent"):
            return "Essential"
        elif self.category in ("Travel", "Entertainment"):
            return "Discretionary"
        else:
            return "Unknown"

    def to_dict(self):
        """Converts this object into a plain text dict - needed for JSON serialization."""
        return {
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "spend_type": self.spend_type,
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Transaction object from a dict."""
        return cls(data["description"], data["amount"], data["category"])

    def __str__(self):
        return f"{self.description:<15} {self.amount:>10.2f}  [{self.category} - {self.spend_type}]"

class FinanceTracker:
    """Manages the Full collection of transactions: loading, saving, and calculating summaries."""

    def __init__(self,income,filename=DATA_FILE):
        self.income =income
        self.filename = filename
        self.transactions = self.load_transactions()

    def load_transactions(self):
        if not self.filename.exists():
            return []
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Transaction.from_dict(t) for t in data]
        except json.JSONDecodeError:
        # file exists but has invalid/empty JSON — start fresh instead of crashing
            print("Warning: data file was empty or corrupted. Starting fresh.")
            return []

    def save_transactions(self):
        with open(self.filename, "w") as f:
            data = [t.to_dict() for t in self.transactions]
            json.dump(data, f, indent=2)

    def add_transaction_interactive(self):
        while True:
            description = input("\nEnter transaction description (or 'done' to finish): ").strip()
            if description.lower() == "done":
                return False
            if description == "":
                print("Description cannot be empty. Please try again.")
                continue
            break

        while True:
            amount_input = input("Enter amount: ")
            try:
                amount = float(amount_input)
                break
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

        category = input("Enter category (Food/Rent/Travel/Other): ").strip().title()
        if category == "":
            category = "Other"

        transaction = Transaction(description, amount, category)
        self.transactions.append(transaction)
        print(f"Added: {transaction}")
        return True

    def calculate_totals(self):
        total_spent = 0
        category_totals = {}
        for t in self.transactions:
            total_spent += t.amount
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount
        return total_spent, category_totals

    def find_highest_category(self,category_totals):
        if not category_totals:
            return None, 0
        highest_category = max(category_totals, key=category_totals.get)
        return highest_category, category_totals[highest_category]

    def calculate_remaining(self, total_spent):
        return self.income - total_spent

    def calculate_percentage_spent(self, total_spent):
        if self.income == 0:
            return 0
        return (total_spent / self.income) * 100

    def print_transaction_list(self):
        print("\n" + "=" * 40)
        print("ALL TRANSACTIONS (including previously saved)")
        print("=" * 40)
        for t in self.transactions:
            print(t)

    def print_summary(self):
        total_spent, category_totals = self.calculate_totals()        
        remaining = self.calculate_remaining(total_spent)
        percentage_spent = self.calculate_percentage_spent(total_spent)

        print("\n" + "=" * 40)
        print(" MONTHLY SUMMARY")
        print("=" * 40)
        print(f"Total Spent: ${total_spent:.2f}")
        print(f"Total Income: ${self.income:.2f}")
        print(f"Percentage of Income Spent: {percentage_spent:.2f}%")
        print(f"Remaining Balance: ${remaining:.2f}")

        if total_spent > self.income:
            print("\n⚠️  You are OVERSPENDING this month!")
        elif percentage_spent > 90:
            print("\n⚠️  You have spent more than 90% of your income!")
        else:
            print("\n✅ You are within your budget.")

    def print_category_breakdown(self):
        total_spent, category_totals = self.calculate_totals()
        highest_category, highest_amount = self.find_highest_category(category_totals)
        
        print("\n" + "=" * 40)
        print(" SPENDING BY CATEGORY")
        print("=" * 40)
        for cat,total in category_totals.items():
            print(f"{cat:<15}: ${total:.2f}")
        if highest_category:
            print(f"\nHighest Spending Category: {highest_category} (${highest_amount:.2f})")

        unique_categories = set(category_totals.keys())
        print(f"You spent across {len(unique_categories)} unique categories this month.")  


def main ():
        print("="* 40)
        print("PERSONAL FINANCE TRACKER - V5 (OOP)")
        print("+"* 40)

        income = float(input("Enter your monthly income: "))
        tracker = FinanceTracker(income)
        if tracker.transactions:
            print(f"\nLoaded {len(tracker.transactions)} transactions from previous sessions.")
        else:
            print("No previous data found -- starting fresh")

        while tracker.add_transaction_interactive():
                pass

        tracker.save_transactions()
        print(f"\n💾 Saved {len(tracker.transactions)} total transaction(s) to {tracker.filename}")

        tracker.print_transaction_list()
        tracker.print_summary()
        tracker.print_category_breakdown()

        print(f"\n(Total Transaction objects created this run: {Transaction.count})")

if __name__ == "__main__":
    main()