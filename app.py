#BANKING MANAGEMENT SYSTEM

import streamlit as st
import time
import hashlib
from decimal import Decimal

from db import conn, cursor, ensure_connection


st.set_page_config(page_title="Banking Management System", page_icon="🏦", layout="centered")

#replaces the global variables accounts and next_account

if "logged_in_acc" not in st.session_state:
    st.session_state.logged_in_acc = None

if "last_deposit_time" not in st.session_state:
    st.session_state.last_deposit_time = 0

if "last_password_change_time" not in st.session_state:
    st.session_state.last_password_change_time = 0


# ─── Helper: hash a password with SHA-256 ───────────────────────────────────

def hash_password(password):
    """Return the SHA-256 hex digest of *password*."""
    return hashlib.sha256(password.encode()).hexdigest()


# ─── Database operations ────────────────────────────────────────────────────

def create_account(name, age, mobile, password):

    ensure_connection()

    sql = """
    INSERT INTO accounts(name,age,mobile,password,balance)
    VALUES(%s,%s,%s,%s,%s)
    """

    values = (name, age, mobile, hash_password(password), 0)

    cursor.execute(sql, values)
    conn.commit()

    return cursor.lastrowid


def verify_login(acc_no, password):

    ensure_connection()

    cursor.execute(
        "SELECT * FROM accounts WHERE account_no=%s",
        (acc_no,)
    )

    account = cursor.fetchone()

    if account is None:
        return "not_found"

    if account["password"] != hash_password(password):
        return "wrong_password"

    return "success"


def do_deposit(acc_no, amount):

    ensure_connection()

    amount = Decimal(str(amount))

    if amount <= 0:
        return False, "Invalid Amount"

    cursor.execute(
        "UPDATE accounts SET balance = balance + %s WHERE account_no=%s",
        (amount, acc_no)
    )

    conn.commit()

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (acc_no,)
    )

    row = cursor.fetchone()
    if row is None:
        return False, "Account not found"

    balance = row["balance"]

    return True, f"Deposit Successful. Current Balance: ₹{balance:.2f}"

def do_withdraw(acc_no, amount):

    ensure_connection()

    amount = Decimal(str(amount))

    if amount <= 0:
        return False, "Invalid Amount"

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (acc_no,)
    )

    row = cursor.fetchone()
    if row is None:
        return False, "Account not found"

    balance = row["balance"]

    if amount > balance:
        return False, "Insufficient Balance"

    cursor.execute(
        "UPDATE accounts SET balance = balance - %s WHERE account_no=%s",
        (amount, acc_no)
    )

    conn.commit()

    return True, f"Withdrawal Successful. Current Balance: ₹{balance - amount:.2f}"


def do_transfer(sender, receiver, amount):

    ensure_connection()

    amount = Decimal(str(amount))

    # ── Validation ──────────────────────────────────────────────────────
    if amount <= 0:
        return False, "Amount must be greater than 0"

    if sender == receiver:
        return False, "Cannot transfer to your own account"

    # ── Check sender balance ────────────────────────────────────────────
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (sender,)
    )

    sender_row = cursor.fetchone()
    if sender_row is None:
        return False, "Sender account not found"

    sender_balance = sender_row["balance"]

    if amount > sender_balance:
        return False, "Insufficient Balance"

    # ── Check receiver exists ───────────────────────────────────────────
    cursor.execute(
        "SELECT * FROM accounts WHERE account_no=%s",
        (receiver,)
    )

    if cursor.fetchone() is None:
        return False, "Receiver Account Not Found"

    # ── Execute transfer inside a transaction ───────────────────────────
    try:
        cursor.execute(
            "UPDATE accounts SET balance=balance-%s WHERE account_no=%s",
            (amount, sender)
        )

        cursor.execute(
            "UPDATE accounts SET balance=balance+%s WHERE account_no=%s",
            (amount, receiver)
        )

        conn.commit()
    except Exception:
        conn.rollback()
        return False, "Transfer failed due to a server error. Please try again."

    return True, "Transfer Successful"


def do_change_password(acc_no, old_pw, new_pw):

    ensure_connection()

    cursor.execute(
        """
        SELECT password
        FROM accounts
        WHERE account_no=%s
        """,
        (acc_no,)
    )

    row = cursor.fetchone()
    if row is None:
        return False, "Account not found"

    password = row["password"]

    if password != hash_password(old_pw):
        return False, "Wrong Password"

    cursor.execute(
        """
        UPDATE accounts
        SET password=%s
        WHERE account_no=%s
        """,
        (hash_password(new_pw), acc_no)
    )

    conn.commit()

    return True, "Password Changed Successfully"

#login or create account

def show_auth_screen():
    st.title("🏦 Banking Management System")

    tab_login, tab_create = st.tabs(["Login", "Create Account"])

    with tab_login:
        st.subheader("Login")
        with st.form("login_form", clear_on_submit=False):
            acc_input = st.text_input("Account Number")
            pw_input = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            if not acc_input.strip().isdigit():
                st.error("Please enter a valid numeric account number.")
            else:
                result = verify_login(int(acc_input), pw_input)
                if result == "not_found":
                    st.error("Account Not Found")
                elif result == "wrong_password":
                    st.error("Wrong Password")
                else:
                    st.session_state.logged_in_acc = int(acc_input)
                    st.success("Login Successful")
                    st.rerun()

    with tab_create:
        st.subheader("Create Account")
        with st.form("create_account_form", clear_on_submit=True):
            name = st.text_input("Enter Name")
            age = st.number_input("Enter Age", min_value=1, max_value=120, step=1)
            mobile = st.text_input("Enter Mobile Number")
            password = st.text_input("Create Password", type="password")
            submitted_create = st.form_submit_button("Create Account")

        if submitted_create:
            if not name.strip() or not mobile.strip() or not password:
                st.error("Please fill in all fields.")
            elif not mobile.strip().isdigit() or len(mobile.strip()) != 10:
                st.error("Mobile number must be exactly 10 digits.")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters long.")
            else:
                acc_no = create_account(name.strip(), int(age), mobile.strip(), password)
                st.success("Account Created Successfully!")
                st.info(f"Your Account Number is **{acc_no}** — save it, you'll need it to log in.")

#customer Menu

def show_customer_dashboard():
    acc = st.session_state.logged_in_acc

    ensure_connection()

    cursor.execute(
    "SELECT * FROM accounts WHERE account_no=%s",
    (acc,)
    )

    info = cursor.fetchone()

    if info is None:
        st.error("Account data not found. Logging out.")
        st.session_state.logged_in_acc = None
        st.rerun()
        return

    st.sidebar.title("🏦 Customer Menu")
    st.sidebar.markdown(f"**{info['name']}**  \nAccount No: `{acc}`")
    st.sidebar.divider()

    menu = st.sidebar.radio(
        "Choose an action",
        [
            "Check Balance",
            "Deposit Money",
            "Withdraw Money",
            "Transfer Money",
            "View Profile",
            "Change Password",
            "Logout",
        ],
        label_visibility="collapsed",
    )

    st.title("🏦 Banking Management System")

    if menu == "Check Balance":
        st.subheader("Current Balance")

        ensure_connection()

        cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (acc,)
        )

        row = cursor.fetchone()
        if row is None:
            st.error("Could not fetch balance.")
        else:
            st.metric("Balance", f"₹{row['balance']:.2f}")


    elif menu == "Deposit Money":
        st.subheader("💰 Deposit Money")

        with st.form("deposit_form", clear_on_submit=True):
            amount = st.text_input(
                "Enter Deposit Amount",
                placeholder="Enter amount and press Enter"
            )
            submitted = st.form_submit_button("Deposit")

        if submitted:
            if time.time() - st.session_state.last_deposit_time < 60:
                st.warning("Please wait 1 minute before making another deposit.")
            elif amount.strip() == "":
                st.error("Please enter an amount.")
            else:
                try:
                    amount = float(amount)
                    if amount <= 0:
                        st.error("Amount must be greater than 0.")
                    else:
                        ok, msg = do_deposit(acc, amount)
                        if ok:
                            st.session_state.last_deposit_time = time.time()
                            st.success(msg)
                        else:
                            st.error(msg)
                except ValueError:
                    st.error("Please enter a valid numeric amount.")


    elif menu == "Withdraw Money":
        st.subheader("Withdraw Money")

        with st.form("withdraw_form", clear_on_submit=True):
            amount = st.text_input(
                "Enter Withdraw Amount",
                placeholder="Enter amount and press Enter"
            )
            submitted = st.form_submit_button("Withdraw")

        if submitted:
            if amount.strip() == "":
                st.error("Please enter an amount.")
            else:
                try:
                    amount = float(amount)
                    if amount <= 0:
                        st.error("Amount must be greater than 0.")
                    else:
                        ok, msg = do_withdraw(acc, amount)
                        (st.success if ok else st.error)(msg)
                except ValueError:
                    st.error("Please enter a valid numeric amount.")

    elif menu == "Transfer Money":
        st.subheader("Transfer Money")
        with st.form("transfer_form", clear_on_submit=True):
            receiver = st.text_input("Enter Receiver Account Number")
            amount = st.text_input(
                "Enter Amount",
                placeholder="Enter amount and press Enter"
            )
            submitted = st.form_submit_button("Transfer")

        if submitted:
            if not receiver.strip().isdigit():
                st.error("Please enter a valid numeric account number.")
            elif amount.strip() == "":
                st.error("Please enter an amount.")
            else:
                try:
                    amount = float(amount)
                    if amount <= 0:
                        st.error("Amount must be greater than 0.")
                    else:
                        ok, msg = do_transfer(acc, int(receiver), amount)
                        (st.success if ok else st.error)(msg)
                except ValueError:
                    st.error("Please enter a valid numeric amount.")

    elif menu == "View Profile":
        st.subheader("Profile")
        st.write(f"**Account Number:** {acc}")
        st.write(f"**Name:** {info['name']}")
        st.write(f"**Age:** {info['age']}")
        st.write(f"**Mobile:** {info['mobile']}")
        st.write(f"**Balance:** ₹{info['balance']:.2f}")

    elif menu == "Change Password":
        st.subheader("Change Password")
        with st.form("change_password_form", clear_on_submit=True):
            old_pw = st.text_input("Enter Old Password", type="password")
            new_pw = st.text_input("Enter New Password", type="password")
            submitted = st.form_submit_button("Change Password")
        if submitted:
            if time.time() - st.session_state.last_password_change_time < 60:
                st.warning("Please wait 1 minute before changing password again.")
            elif not old_pw.strip() or not new_pw.strip():
                st.error("Please fill in both password fields.")
            elif len(new_pw) < 4:
                st.error("New password must be at least 4 characters long.")
            else:
                ok, msg = do_change_password(acc, old_pw, new_pw)
                if ok:
                    st.session_state.last_password_change_time = time.time()
                    st.success(msg)
                else:
                    st.error(msg)

    elif menu == "Logout":
        st.session_state.logged_in_acc = None
        st.success("Logged Out Successfully")
        st.rerun()



#replaces the while True: menu loop

if st.session_state.logged_in_acc is None:
    show_auth_screen()
else:
    show_customer_dashboard()
