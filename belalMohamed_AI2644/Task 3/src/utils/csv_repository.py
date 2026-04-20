import csv
import os
from typing import Optional

from user import User
from transaction import Transaction
from interfaces import IUserRepository, ITransactionRepository

USER_FIELDS = ["user_id", "name", "password", "phone", "balance", "created_at"]
TRANSACTION_FIELDS = [
    "transaction_id", "user_id", "transaction_type",
    "amount", "balance_after", "description", "timestamp"
]

class CSVUserRepository(IUserRepository):

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
                writer.writeheader()

    def _read_all_rows(self) -> list[dict]:
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_all_rows(self, rows: list[dict]) -> None:
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
            writer.writeheader()
            writer.writerows(rows)


    def save_user(self, user: User) -> None:
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
            writer.writerow(user.to_dict())

    def update_user(self, user: User) -> None:
        rows = self._read_all_rows()
        updated = []
        for r in rows:
            if r["user_id"] == user.user_id:
                updated.append(user.to_dict())
            else:
                updated.append(r)
        self._write_all_rows(updated)

    def delete_user(self, user_id: str) -> None:
        rows = self._read_all_rows()
        filtered = []
        for r in rows:
            if r["user_id"] != user_id:
                filtered.append(r)
        self._write_all_rows(filtered)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        for row in self._read_all_rows():
            if row["user_id"] == user_id:
                return User.from_dict(row)
        return None

    def get_all_users(self) -> list[User]:
        users = []
        for row in self._read_all_rows():
            users.append(User.from_dict(row))
        return users 


class CSVTransactionRepository(ITransactionRepository):

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
                writer.writeheader()

    def save_transaction(self, transaction: Transaction) -> None:
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
            writer.writerow(transaction.to_dict())

    def get_transactions_by_user(self, user_id: str) -> list[Transaction]:
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        transactions = [Transaction.from_dict(r) for r in rows if r["user_id"] == user_id]
        return sorted(transactions, key=lambda t: t.timestamp, reverse=True) # Sort newest first

    def get_all_transactions(self) -> list[Transaction]:
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        transactions = [Transaction.from_dict(r) for r in rows]
        return sorted(transactions, key=lambda t: t.timestamp, reverse=True)
