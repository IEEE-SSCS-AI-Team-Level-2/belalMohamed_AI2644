"""
HOW TO RUN:
    python -m pytest tests/
    python -m unittest discover tests
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.bank_system import BankSystem, BankingError
from src.models.user import User
from src.models.transaction import Transaction
from src.services.interfaces import IUserRepository, ITransactionRepository

class MockUserRepository(IUserRepository):

    def __init__(self):
        self._users: dict[str, User] = {}

    def save_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def update_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def delete_user(self, user_id: str) -> None:
        self._users.pop(user_id, None)

    def get_user_by_id(self, user_id: str):
        return self._users.get(user_id)

    def get_all_users(self) -> list:
        return list(self._users.values())


class MockTransactionRepository(ITransactionRepository):
    def __init__(self):
        self._transactions: list[Transaction] = []

    def save_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def get_transactions_by_user(self, user_id: str) -> list:
        return [t for t in self._transactions if t.user_id == user_id]

    def get_all_transactions(self) -> list:
        return self._transactions.copy()


# Test Cases
class TestBankSystem(unittest.TestCase):

    def setUp(self):
        # creates a fresh BankSystem
        self.bank = BankSystem(
            user_repo=MockUserRepository(),
            transaction_repo=MockTransactionRepository(),
        )

    # Account Creation

    def test_create_account_success(self):
        user = self.bank.create_account("Ahmed Hassan", "pass123", "01012345678", 500.0)
        self.assertEqual(user.name, "Ahmed Hassan")
        self.assertEqual(user.balance, 500.0)
        self.assertTrue(user.user_id.startswith("USR-"))

    def test_create_account_short_password(self):
        with self.assertRaises(BankingError):
            self.bank.create_account("Ahmed", "123", "01012345678")

    def test_create_account_invalid_phone(self):
        with self.assertRaises(BankingError):
            self.bank.create_account("Ahmed", "pass123", "123")

    def test_create_account_negative_balance(self):
        with self.assertRaises(BankingError):
            self.bank.create_account("Ahmed", "pass123", "01012345678", -100)

    def test_password_is_hashed(self):
        user = self.bank.create_account("Ahmed", "pass123", "01012345678")
        self.assertNotEqual(user.password, "pass123") 

    # Deposit

    def test_deposit_success(self):
        user = self.bank.create_account("Sara", "pass123", "01098765432", 0)
        updated = self.bank.deposit(user.user_id, 1000.0)
        self.assertEqual(updated.balance, 1000.0)

    def test_deposit_zero_raises(self):
        user = self.bank.create_account("Sara", "pass123", "01098765432")
        with self.assertRaises(BankingError):
            self.bank.deposit(user.user_id, 0)

    def test_deposit_negative_raises(self):
        user = self.bank.create_account("Sara", "pass123", "01098765432")
        with self.assertRaises(BankingError):
            self.bank.deposit(user.user_id, -50)

    # Withdrawal

    def test_withdraw_success(self):
        user = self.bank.create_account("Mina", "pass123", "01112345678", 500)
        updated = self.bank.withdraw(user.user_id, 200)
        self.assertEqual(updated.balance, 300.0)

    def test_withdraw_insufficient_funds(self):
        user = self.bank.create_account("Mina", "pass123", "01112345678", 100)
        with self.assertRaises(BankingError):
            self.bank.withdraw(user.user_id, 500)

    # Delete

    def test_delete_account_success(self):
        user = self.bank.create_account("Layla", "mypassword", "01234567890")
        self.bank.delete_account(user.user_id, "mypassword")
        with self.assertRaises(BankingError):
            self.bank.get_user(user.user_id)

    def test_delete_wrong_password(self):
        user = self.bank.create_account("Layla", "mypassword", "01234567890")
        with self.assertRaises(BankingError):
            self.bank.delete_account(user.user_id, "wrongpassword")

    # Transaction History

    def test_transaction_recorded_on_deposit(self):
        user = self.bank.create_account("Omar", "pass123", "01098760000", 0)
        self.bank.deposit(user.user_id, 500)
        history = self.bank.get_transaction_history(user.user_id)
        # should have 2 transactions: account creation + deposit
        self.assertGreaterEqual(len(history), 2)

    # Update

    def test_update_name(self):
        user = self.bank.create_account("Old Name", "pass123", "01012345678")
        updated = self.bank.update_name(user.user_id, "New Name")
        self.assertEqual(updated.name, "New Name")

    def test_update_password_wrong_old_password(self):
        user = self.bank.create_account("Test", "correct123", "01012345678")
        with self.assertRaises(BankingError):
            self.bank.update_password(user.user_id, "wrongpass", "newpass123")


if __name__ == "__main__":
    unittest.main()