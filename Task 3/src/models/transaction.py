from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    DEPOSIT    = "Deposit"
    WITHDRAWAL = "Withdrawal"
    CREATE     = "Account Created"
    DELETE     = "Account Deleted"
    UPDATE     = "Account Updated"

@dataclass
class Transaction:

    transaction_id:   str
    user_id:          str
    transaction_type: str  
    amount:           float
    balance_after:    float
    description:      str = ""
    timestamp:        str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    def __str__(self) -> str:
        return (
            f"[{self.timestamp}] {self.transaction_type} | "
            f"Amount: {self.amount:.2f} EGP | "
            f"Balance After: {self.balance_after:.2f} EGP"
        )

    def to_dict(self) -> dict:
        return {
            "transaction_id":   self.transaction_id,
            "user_id":          self.user_id,
            "transaction_type": self.transaction_type,
            "amount":           self.amount,
            "balance_after":    self.balance_after,
            "description":      self.description,
            "timestamp":        self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            transaction_id=data["transaction_id"],
            user_id=data["user_id"],
            transaction_type=data["transaction_type"],
            amount=float(data["amount"]),
            balance_after=float(data["balance_after"]),
            description=data.get("description", ""),
            timestamp=data.get("timestamp", ""),
        )