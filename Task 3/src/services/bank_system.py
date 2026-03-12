import hashlib
import uuid
from typing import Optional

from user import User
from transaction import Transaction, TransactionType
from interfaces import IUserRepository, ITransactionRepository


class BankingError(Exception):
    pass


class BankSystem:
    
    def __init__(
        self,
        user_repo: IUserRepository,
        transaction_repo: ITransactionRepository,
    ) -> None:
        self._user_repo = user_repo
        self._transaction_repo = transaction_repo

# PRIVATE METHODS

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _generate_user_id(self) -> str:
        users = self._user_repo.get_all_users()
        next_num = len(users) + 1
        return f"USR-{next_num:04d}"

    def _generate_transaction_id(self) -> str:
        return f"TRANS-{uuid.uuid4().hex[:8].upper()}"

    def _record_transaction(
        self,
        user_id: str,
        txn_type: TransactionType,
        amount: float,
        balance_after: float,
        description: str = "",
    ) -> None:
        
        txn = Transaction(
            transaction_id=self._generate_transaction_id(),
            user_id=user_id,
            transaction_type=txn_type.value,
            amount=amount,
            balance_after=balance_after,
            description=description,
        )
        self._transaction_repo.save_transaction(txn)

    def _get_user_or_raise(self, user_id: str) -> User:
        user = self._user_repo.get_user_by_id(user_id)
        if user is None:
            raise BankingError(f"No account found with ID: {user_id}")
        return user

# PUBLIC METHODS

    def create_account(
        self,
        name: str,
        password: str,
        phone: str,
        initial_balance: float = 0.0,
    ) -> User:

        name = name.strip()
        phone = phone.strip()

        if not name:
            raise BankingError("Name cannot be empty.")
        if not password or len(password) < 6 or not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            raise BankingError("Password must be at least 6 characters and contain both letters and numbers.")
        if not phone or not phone.isdigit() or len(phone) < 10:
            raise BankingError("Phone must be at least 10 digits.")
        if initial_balance < 0:
            raise BankingError("Initial balance cannot be negative.")

        user = User(
            user_id=self._generate_user_id(),
            name=name,
            password=self._hash_password(password),
            phone=phone,
            balance=initial_balance,
        )
        self._user_repo.save_user(user)
        self._record_transaction(
            user_id=user.user_id,
            txn_type=TransactionType.CREATE,
            amount=initial_balance,
            balance_after=initial_balance,
            description="Account opened.",
        )
        return user

    def delete_account(self, user_id: str, password: str) -> None:

        user = self._get_user_or_raise(user_id)

        if user.password != self._hash_password(password):
            raise BankingError("Incorrect password.")

        self._record_transaction(
            user_id=user_id,
            txn_type=TransactionType.DELETE,
            amount=0,
            balance_after=0,
            description="Account closed.",
        )
        self._user_repo.delete_user(user_id)

    def update_name(self, user_id: str, new_name: str) -> User:
        user = self._get_user_or_raise(user_id)
        new_name = new_name.strip()
        if not new_name:
            raise BankingError("Name cannot be empty.")

        old_name = user.name
        user.name = new_name
        self._user_repo.update_user(user)
        self._record_transaction(
            user_id=user_id,
            txn_type=TransactionType.UPDATE,
            amount=0,
            balance_after=user.balance,
            description=f"Name changed from '{old_name}' to '{new_name}'.",
        )
        return user

    def update_password(self, user_id: str, old_password: str, new_password: str) -> User:
        user = self._get_user_or_raise(user_id)

        if user.password != self._hash_password(old_password):
            raise BankingError("Incorrect current password.")
        if len(new_password) < 6 or not any(c.isdigit() for c in new_password) or not any(c.isalpha() for c in new_password):
            raise BankingError("New password must be at least 6 characters and contain both letters and numbers.")

        user.password = self._hash_password(new_password)
        self._user_repo.update_user(user)
        self._record_transaction(
            user_id=user_id,
            txn_type=TransactionType.UPDATE,
            amount=0,
            balance_after=user.balance,
            description="Password updated.",
        )
        return user

    def update_phone(self, user_id: str, new_phone: str) -> User:
        user = self._get_user_or_raise(user_id)
        new_phone = new_phone.strip()
        if not new_phone.isdigit() or len(new_phone) < 10:
            raise BankingError("Phone must be at least 10 digits.")

        user.phone = new_phone
        self._user_repo.update_user(user)
        self._record_transaction(
            user_id=user_id,
            txn_type=TransactionType.UPDATE,
            amount=0,
            balance_after=user.balance,
            description=f"Phone updated to {new_phone}.",
        )
        return user

    def deposit(self, user_id: str, amount: float) -> User:
        if amount <= 0:
            raise BankingError("Deposit amount must be greater than zero.")

        user = self._get_user_or_raise(user_id)
        user.balance += amount
        self._user_repo.update_user(user)
        self._record_transaction(
            user_id=user_id,
            txn_type=TransactionType.DEPOSIT,
            amount=amount,
            balance_after=user.balance,
            description=f"Deposited {amount:.2f} EGP.",
        )
        return user

    def withdraw(self, user_id: str, amount: float) -> User:
        if amount <= 0:
            raise BankingError("Withdrawal amount must be greater than zero.")

        user = self._get_user_or_raise(user_id)

        if amount > user.balance:
            raise BankingError(
                f"Insufficient funds. Balance: {user.balance:.2f} EGP, "
                f"Requested: {amount:.2f} EGP."
            )

        user.balance -= amount
        self._user_repo.update_user(user)
        self._record_transaction(
            user_id=user_id,
            txn_type=TransactionType.WITHDRAWAL,
            amount=amount,
            balance_after=user.balance,
            description=f"Withdrew {amount:.2f} EGP.",
        )
        return user

    def get_user(self, user_id: str) -> User:
        return self._get_user_or_raise(user_id)

    def get_all_users(self) -> list[User]:
        return self._user_repo.get_all_users()

    def get_transaction_history(self, user_id: str) -> list[Transaction]:
        self._get_user_or_raise(user_id)
        return self._transaction_repo.get_transactions_by_user(user_id)

    def get_all_transactions(self) -> list[Transaction]:
        return self._transaction_repo.get_all_transactions()

    def verify_password(self, user_id: str, password: str) -> bool:
        user = self._user_repo.get_user_by_id(user_id)
        if user is None:
            return False
        return user.password == self._hash_password(password)
