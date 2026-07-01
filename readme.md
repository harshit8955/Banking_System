# 🏦 Banking Management System

A simple **Banking Management System** built using **Core Python** without any external libraries, SQL databases, or file handling. This project is designed for beginners to practice Python programming by creating a menu-driven banking application.

---

# 📌 Project Overview

This project simulates the basic operations of a bank. Users can create an account, log in securely, and perform banking transactions such as depositing money, withdrawing money, transferring funds, checking their balance, viewing their profile, and changing their password.

All account information is stored in Python dictionaries while the program is running.

> **Note:** Since no database or file storage is used, all data is lost when the program is closed.

---

# ✨ Features

* Create a New Bank Account
* Login with Account Number and Password
* Check Account Balance
* Deposit Money
* Withdraw Money
* Transfer Money to Another Account
* View Customer Profile
* Change Password
* Logout
* Exit Application

---

# 🛠 Technologies Used

* Python 3
* Core Python Only

No external libraries are required.

---

# 📚 Python Concepts Used

* Variables
* Data Types
* Input and Output
* Conditional Statements (`if`, `elif`, `else`)
* Loops (`while`)
* Functions
* Dictionaries
* Nested Dictionaries
* Menu-Driven Programming

---

# 📂 Project Structure

```text
Banking_System/
│
├── main.py
└── README.md
```

---

# 📊 Account Data Structure

Each account is stored as a nested dictionary.

```python
accounts = {
    1001: {
        "name": "Harshit",
        "age": 21,
        "mobile": "9876543210",
        "password": "1234",
        "balance": 5000
    }
}
```

---

# 📋 Main Menu

```text
==============================
   BANKING MANAGEMENT SYSTEM
==============================

1. Create Account
2. Login
3. Exit
```

---

# 👤 Customer Menu

```text
==============================
      CUSTOMER MENU
==============================

1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Transfer Money
5. View Profile
6. Change Password
7. Logout
```

---

# ⚙ Functional Modules

## Account Management

* Create Account
* Login
* Logout
* Change Password
* View Profile

## Banking Operations

* Check Balance
* Deposit Money
* Withdraw Money
* Transfer Money

---

# 🔄 Program Workflow

```text
Start
   │
   ▼
Main Menu
   │
   ├── Create Account
   │
   ├── Login
   │      │
   │      ▼
   │  Customer Menu
   │      │
   │      ├── Check Balance
   │      ├── Deposit Money
   │      ├── Withdraw Money
   │      ├── Transfer Money
   │      ├── View Profile
   │      ├── Change Password
   │      └── Logout
   │
   └── Exit
```

---

# ▶ How to Run

1. Install **Python 3**.
2. Download or clone this project.
3. Open a terminal in the project folder.
4. Run the program:

```bash
python main.py
```

---

# 📝 Example Usage

### Create an Account

* Enter Name
* Enter Age
* Enter Mobile Number
* Create Password
* Receive an automatically generated Account Number

### Login

* Enter Account Number
* Enter Password

### Banking Operations

* Check current balance
* Deposit money
* Withdraw money
* Transfer money
* View profile
* Change password
* Logout

---

# ⚠ Limitations

* Data is stored only in memory.
* Closing the program deletes all account data.
* No database integration.
* No file storage.
* Single-user console application.

---

# 🚀 Future Enhancements

* Save data using JSON files
* Transaction history
* Account number validation
* Mobile number validation
* Password strength checking
* PIN authentication
* Interest calculator
* Loan calculator
* Mini statement
* Console UI improvements

---

# 🎯 Learning Outcomes

By completing this project, you will learn:

* Core Python programming
* Menu-driven application development
* Function-based programming
* Dictionary data structures
* Basic banking transaction logic
* Problem-solving using Python

---

# 📄 License

This project is developed for educational purposes and beginner-level Python practice.
