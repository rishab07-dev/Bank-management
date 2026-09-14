import json
import hashlib
import secrets
import string
from pathlib import Path
from datetime import datetime 

 #improvisedd code for bank management system with better security and features

class Bank:
    DATABASE = Path("data.json")

    def __init__(self):
        self.data = self._load_data()

    # -----------------------------
    # Database methods
    # -----------------------------

    def _load_data(self):
        try:
            if not self.DATABASE.exists():
                self.DATABASE.write_text("[]", encoding="utf-8")
                return []

            with open(self.DATABASE, "r", encoding="utf-8") as file:
                data = json.load(file)

                if not isinstance(data, list):
                    return []

                return data

        except (json.JSONDecodeError, OSError):
            return []

    def _save_data(self):
        temp_file = self.DATABASE.with_suffix(".tmp")

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

        temp_file.replace(self.DATABASE)

    # -----------------------------
    # Utility methods
    # -----------------------------

    @staticmethod
    def _hash_pin(pin):
        return hashlib.sha256(str(pin).encode()).hexdigest()

    @staticmethod
    def _generate_account_number():
        """
        Generates an account number like:
        AB7K9P42
        """

        characters = string.ascii_uppercase + string.digits

        while True:
            account_number = "".join(
                secrets.choice(characters)
                for _ in range(8)
            )

            return account_number

    def _find_account(self, account_number):
        for account in self.data:
            if account["account_number"] == account_number:
                return account

        return None

    def authenticate(self, account_number, pin):
        account = self._find_account(account_number)

        if not account:
            return None

        hashed_pin = self._hash_pin(pin)

        if account["pin"] != hashed_pin:
            return None

        return account

    # -----------------------------
    # Create account
    # -----------------------------

    def create_account(self, name, age, email, pin):

        name = name.strip()
        email = email.strip()

        if not name:
            return False, "Name cannot be empty."

        if age < 18:
            return False, "You must be at least 18 years old."

        if not email:
            return False, "Email cannot be empty."

        if not pin.isdigit() or len(pin) != 4:
            return False, "PIN must contain exactly 4 digits."

        # Check if email already exists
        for account in self.data:
            if account["email"].lower() == email.lower():
                return False, "An account with this email already exists."

        account_number = self._generate_account_number()

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": self._hash_pin(pin),
            "account_number": account_number,
            "balance": 0.0,
            "transactions": [
                {
                    "type": "Account Created",
                    "amount": 0.0,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }

        self.data.append(account)
        self._save_data()

        return True, account_number

    # -----------------------------
    # Deposit
    # -----------------------------

    def deposit(self, account_number, pin, amount):

        account = self.authenticate(account_number, pin)

        if not account:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Deposit amount must be greater than ₹0."

        if amount > 10000:
            return False, "Maximum deposit per transaction is ₹10,000."

        account["balance"] += amount

        account["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._save_data()

        return True, account["balance"]

    # -----------------------------
    # Withdraw
    # -----------------------------

    def withdraw(self, account_number, pin, amount):

        account = self.authenticate(account_number, pin)

        if not account:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Withdrawal amount must be greater than ₹0."

        if amount > account["balance"]:
            return False, "Insufficient balance."

        account["balance"] -= amount

        account["transactions"].append({
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._save_data()

        return True, account["balance"]

    # -----------------------------
    # Get account
    # -----------------------------

    def get_account(self, account_number, pin):

        account = self.authenticate(account_number, pin)

        if not account:
            return None

        return account

    # -----------------------------
    # Update account
    # -----------------------------

    def update_account(
        self,
        account_number,
        pin,
        name=None,
        email=None,
        new_pin=None
    ):

        account = self.authenticate(account_number, pin)

        if not account:
            return False, "Invalid account number or PIN."

        if name and name.strip():
            account["name"] = name.strip()

        if email and email.strip():

            for other_account in self.data:

                if (
                    other_account["email"].lower() == email.lower()
                    and other_account["account_number"] != account_number
                ):
                    return False, "This email is already being used."

            account["email"] = email.strip()

        if new_pin:

            if not new_pin.isdigit() or len(new_pin) != 4:
                return False, "New PIN must contain exactly 4 digits."

            account["pin"] = self._hash_pin(new_pin)

        self._save_data()

        return True, "Account updated successfully."

    # -----------------------------
    # Delete account
    # -----------------------------

    def delete_account(self, account_number, pin):

        account = self.authenticate(account_number, pin)

        if not account:
            return False, "Invalid account number or PIN."

        if account["balance"] > 0:
            return False, (
                "You cannot delete an account with a remaining balance."
            )

        self.data.remove(account)

        self._save_data()

        return True, "Account deleted successfully."

    # -----------------------------
    # Statistics
    # -----------------------------

    def get_statistics(self):

        total_accounts = len(self.data)

        total_balance = sum(
            account["balance"]
            for account in self.data
        )

        return {
            "total_accounts": total_accounts,
            "total_balance": total_balance
        }