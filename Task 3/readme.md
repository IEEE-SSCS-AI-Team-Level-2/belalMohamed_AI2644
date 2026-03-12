# 🏦 NileBank — Complete Banking System

> A full-stack banking system built with Python OOP and SOLID principles, featuring a Streamlit web interface and CSV-based data persistence.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit&logoColor=white)
![OOP](https://img.shields.io/badge/Design-OOP%20%2B%20SOLID-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Overview

NileBank is a complete banking management system built from scratch using Object-Oriented Programming (OOP) and the SOLID design principles. It includes a clean web interface powered by Streamlit and persists all data in CSV files.

This project was built as part of the **IEEE SSCS AI Team Task 3** and is designed to demonstrate professional-grade Python code structure, SOLID architecture, and separation of concerns.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🆕 Create Account | Register a new user with hashed password storage |
| 🔍 View Account | Look up any account by ID |
| 💰 Deposit | Add money to an account |
| 🏧 Withdraw | Withdraw with balance validation |
| ✏️ Update | Change name, phone, or password securely |
| 🗑️ Delete | Remove an account with password confirmation |
| 📜 Transaction History | Full audit trail per user |
| 📊 Admin Dashboard | View all accounts and system-wide stats |
| 💾 Data Persistence | All data saved to CSV, reloaded on startup |

---

## 🗂️ Project Structure

```
banking-system/
│
├── app.py                      # Streamlit web interface (UI only)
│
├── src/
│   ├── models/
│   │   ├── user.py             # User data model (@dataclass)
│   │   └── transaction.py      # Transaction model + TransactionType Enum
│   │
│   ├── services/
│   │   ├── interfaces.py       # Abstract base classes (SOLID: I + D)
│   │   └── bank_system.py      # Core banking logic (SOLID: S + O)
│   │
│   └── utils/
│       └── csv_repository.py   # CSV storage implementation (SOLID: D)
│
├── data/
│   ├── users.csv               # Auto-created on first run
│   └── transactions.csv        # Auto-created on first run
│
├── tests/
│   └── test_bank_system.py     # Unit tests
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧱 OOP Concepts Used

| Concept | Where Used |
|---|---|
| **Classes & Instance Attributes** | `User`, `Transaction`, `BankSystem` |
| **`@dataclass`** | `User`, `Transaction` — clean boilerplate-free models |
| **Magic/Dunder Methods** | `__str__`, `__repr__` on `User` and `Transaction` |
| **Class Methods** | `User.from_dict()`, `Transaction.from_dict()` — alternative constructors |
| **Encapsulation** | Private helpers `_hash_password`, `_get_user_or_raise` in `BankSystem` |
| **Inheritance** | `CSVUserRepository` inherits from `IUserRepository` |
| **Abstract Base Classes** | `IUserRepository`, `ITransactionRepository` in `interfaces.py` |
| **Polymorphism** | `BankSystem` accepts any `IUserRepository` — CSV, DB, mock |
| **Enum** | `TransactionType` for type-safe operation categorization |
| **Custom Exception** | `BankingError` for precise error handling |
| **Composition** | `BankSystem` has-a repository (not inherits-from) |

---

## 🏛️ SOLID Principles

### S — Single Responsibility
Each class has exactly one reason to change:
- `User` → stores user data only
- `BankSystem` → banking logic only
- `CSVUserRepository` → CSV file operations only
- `app.py` → UI only

### O — Open/Closed
`TransactionType` (Enum) can be extended with new types without modifying any existing code.

### L — Liskov Substitution
`CSVUserRepository` can be dropped in anywhere an `IUserRepository` is expected — without breaking anything.

### I — Interface Segregation
Storage is split into `IUserRepository` and `ITransactionRepository` — classes only implement what they need.

### D — Dependency Inversion
`BankSystem` depends on **abstractions** (`IUserRepository`), not on `CSVUserRepository` directly. Swap the storage backend by changing two lines in `app.py`.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/banking-system.git
cd banking-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🔒 Security Notes

- Passwords are **never stored in plain text** — they are hashed with SHA-256 before being saved.
- Account deletion requires password confirmation.
- Password updates require the current password.

---

## 🛠️ Tech Stack

- **Python 3.11+** — Core language
- **Streamlit** — Web interface
- **CSV (stdlib)** — Data persistence
- **hashlib (stdlib)** — Password hashing
- **dataclasses (stdlib)** — Clean model definitions
- **abc (stdlib)** — Abstract base classes for SOLID interfaces

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

*Built with ❤️ for the IEEE SSCS AI Team*