from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:

    user_id: str
    name: str
    password: str
    phone: str
    balance: float = 0.0   
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __str__(self) -> str:
        return (
            f"User(ID={self.user_id}, Name={self.name}, "
            f"Phone={self.phone}, Balance={self.balance:.2f} EGP)"
        )

    def __repr__(self) -> str:
        return (
            f"User(user_id={self.user_id!r}, name={self.name!r}, "
            f"phone={self.phone!r}, balance={self.balance!r})"
        )

    def to_dict(self) -> dict:
        return {
            "user_id":    self.user_id,
            "name":       self.name,
            "password":   self.password,
            "phone":      self.phone,
            "balance":    self.balance,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            password=data["password"],
            phone=data["phone"],
            balance=float(data["balance"]),
            created_at=data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )