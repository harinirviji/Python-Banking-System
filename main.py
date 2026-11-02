
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod


# Base class
class BankAccount(ABC):
    def __init__(self, name, number, balance):
        self.name = name
        self.number = number
        self.__balance = balance
        self.history = [f"Account created: Rs.{balance:.2f}"]

    def deposit(self, amount):
        if amount <= 0:
            return False
        self.__balance += amount
        self.history.append(f"Deposited: Rs.{amount:.2f}")
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        self.history.append(f"Withdrawn: Rs.{amount:.2f}")
        return True

    def get_balance(self):
        return self.__balance

    @abstractmethod
    def account_type(self):
        pass


# Inheritance
class SavingsAccount(BankAccount):
    def account_type(self):
        return "Savings Account"


class CurrentAccount(BankAccount):
    def account_type(self):
        return "Current Account"


# Store accounts
accounts = {}


# Create account
def create_account():
    name = name_entry.get().strip()
    number = number_entry.get().strip()
    account_type = type_box.get()
    
    try:
        balance = float(balance_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid opening balance.")
        return

    if not name or not number:
        messagebox.showerror("Error", "Enter name and account number.")
        return

    if number in accounts:
        messagebox.showerror("Error", "Account already exists.")
        return

    if balance < 0:
        messagebox.showerror("Error", "Balance cannot be negative.")
        return

    if account_type == "Savings":
        account = SavingsAccount(name, number, balance)
    else:
        account = CurrentAccount(name, number, balance)

    accounts[number] = account
    messagebox.showinfo("Success", "Account created successfully!")
    show_details(account)


# Find account
def find_account():
    number = number_entry.get().strip()
    account = accounts.get(number)

    if account is None:
        messagebox.showerror("Error", "Account not found.")
        return None

    return account


# Deposit money
def deposit_money():
    account = find_account()
    if account is None:
        return

    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount.")
        return

    if account.deposit(amount):
        show_details(account)
        messagebox.showinfo("Success", "Money deposited successfully!")
    else:
        messagebox.showerror("Error", "Amount must be greater than zero.")


# Withdraw money
def withdraw_money():
    account = find_account()
    if account is None:
        return

    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount.")
        return

    if account.withdraw(amount):
        show_details(account)
        messagebox.showinfo("Success", "Money withdrawn successfully!")
    else:
        messagebox.showerror(
            "Error", "Invalid amount or insufficient balance."
        )


# Check balance and transaction history
def show_details(account=None):
    if account is None:
        account = find_account()
        if account is None:
            return

    output.delete("1.0", tk.END)
    output.insert(tk.END, "PYTHON BANKING SYSTEM\n")
    output.insert(tk.END, "------------------------------\n")
    output.insert(tk.END, f"Name: {account.name}\n")
    output.insert(tk.END, f"Account Number: {account.number}\n")
    output.insert(tk.END, f"Account Type: {account.account_type()}\n")
    output.insert(
        tk.END, f"Balance: Rs.{account.get_balance():.2f}\n\n"
    )
    output.insert(tk.END, "TRANSACTION HISTORY\n")
    output.insert(tk.END, "------------------------------\n")

    for item in account.history:
        output.insert(tk.END, item + "\n")


# Clear fields
def clear_fields():
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    balance_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    output.delete("1.0", tk.END)


# Tkinter window
root = tk.Tk()
root.title("Python Banking System")
root.geometry("500x650")
root.configure(bg="#EAF2F8")

tk.Label(
    root, text="PYTHON BANKING SYSTEM",
    font=("Arial", 18, "bold"), bg="#EAF2F8"
).pack(pady=15)

form = tk.Frame(root, bg="#EAF2F8")
form.pack(padx=20, fill="x")

tk.Label(form, text="Account Holder Name:", bg="#EAF2F8").grid(
    row=0, column=0, sticky="w", pady=5
)
name_entry = tk.Entry(form, width=25)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(form, text="Account Number:", bg="#EAF2F8").grid(
    row=1, column=0, sticky="w", pady=5
)
number_entry = tk.Entry(form, width=25)
number_entry.grid(row=1, column=1, pady=5)

tk.Label(form, text="Opening Balance:", bg="#EAF2F8").grid(
    row=2, column=0, sticky="w", pady=5
)
balance_entry = tk.Entry(form, width=25)
balance_entry.grid(row=2, column=1, pady=5)

tk.Label(form, text="Account Type:", bg="#EAF2F8").grid(
    row=3, column=0, sticky="w", pady=5
)
type_box = ttk.Combobox(
    form, values=["Savings", "Current"],
    state="readonly", width=22
)
type_box.current(0)
type_box.grid(row=3, column=1, pady=5)

tk.Label(form, text="Transaction Amount:", bg="#EAF2F8").grid(
    row=4, column=0, sticky="w", pady=5
)
amount_entry = tk.Entry(form, width=25)
amount_entry.grid(row=4, column=1, pady=5)

buttons = tk.Frame(root, bg="#EAF2F8")
buttons.pack(pady=12)

tk.Button(
    buttons, text="Create Account", command=create_account,
    width=16, bg="#1976D2", fg="white"
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    buttons, text="Deposit", command=deposit_money,
    width=12
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    buttons, text="Withdraw", command=withdraw_money,
    width=12
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    buttons, text="Check Balance", command=show_details,
    width=16
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    buttons, text="Clear", command=clear_fields,
    width=12
).grid(row=2, column=0, padx=5, pady=5)

tk.Button(
    buttons, text="Exit", command=root.destroy,
    width=12
).grid(row=2, column=1, padx=5, pady=5)

output = tk.Text(root, height=13, width=52, font=("Arial", 10))
output.pack(padx=15, pady=10)

root.mainloop()
      
