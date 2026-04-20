from abc import ABC, abstractmethod
from typing import Optional
from user import User
from transaction import Transaction

class IUserRepository(ABC):

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass


class ITransactionRepository(ABC):

    @abstractmethod
    def save_transaction(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def get_transactions_by_user(self, user_id: str) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions(self) -> list[Transaction]:
        pass