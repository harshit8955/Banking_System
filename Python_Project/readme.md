# 🏦 Banking Management System

A Banking Management System built using **Python**, **Streamlit**, and **MySQL**. This project allows users to create bank accounts, securely log in, manage their balance, transfer money, and update account information through a simple web interface.

---

## 🚀 Features

* Create a new bank account
* Auto-generated account number
* Secure login using account number and password
* Deposit money
* Withdraw money
* Transfer money between accounts
* Check account balance
* View customer profile
* Change account password
* Logout functionality
* Data stored permanently in MySQL database

---

## 🛠️ Technologies Used

* Python 3.x
* Streamlit
* MySQL
* mysql-connector-python

---

## 📁 Project Structure

```text
Banking-Management-System/
│
├── main.py                 # Main Streamlit application
├── database.py             # MySQL database connection
├── banking_db.sql          # Database creation script
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Banking-Management-System.git
cd Banking-Management-System
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL and execute the `banking_db.sql` file.

### 5. Configure the database connection

Edit `database.py` and update your MySQL credentials:

```python
host = "localhost"
user = "root"
password = "your_password"
database = "banking_db"
```

### 6. Run the application

```bash
streamlit run main.py
```

---

## 💾 Database

The project uses a MySQL database to store customer account information permanently.

Stored information includes:

* Account Number
* Customer Name
* Age
* Mobile Number
* Password
* Account Balance

---

## 📦 Python Packages

* streamlit
* mysql-connector-python

Install them using:

```bash
pip install -r requirements.txt
```

---

## 📸 Screens

* Login
* Create Account
* Customer Dashboard
* Deposit Money
* Withdraw Money
* Transfer Money
* Profile
* Change Password

---

## 🔮 Future Enhancements

* PIN-based authentication
* Password hashing with bcrypt
* Transaction history
* Admin dashboard
* Mini statement
* Email/SMS notifications
* Interest calculation
* Fixed deposit management
* Loan management
* User profile editing
* PDF account statements

---

## 👨‍💻 Author

**Harshit Sharma**

Computer Science Engineering Student

---

## 📄 License

This project is developed for educational and learning purposes.
