#BANKING MANAGEMENT SYSTEM

import streamlit as st


st.set_page_config(page_title="Banking Management System", page_icon="🏦", layout="centered")

#replaces the global variables accounts and next_account

if "logged_in_acc" not in st.session_state:
    st.session_state.logged_in_acc = None   
    

from db import conn, cursor

def create_account(name, age, mobile, password):

    sql = """
    INSERT INTO accounts(name,age,mobile,password,balance)
    VALUES(%s,%s,%s,%s,%s)
    """

    values = (name, age, mobile, password, 0)

    cursor.execute(sql, values)
    conn.commit()

    return cursor.lastrowid


def verify_login(acc_no, password):

    cursor.execute(
        "SELECT * FROM accounts WHERE account_no=%s",
        (acc_no,)
    )

    account = cursor.fetchone()

    if account is None:
        return "not_found"


    if account["password"] != password:
        return "wrong_password"

    return "success"

def do_deposit(acc_no, amount):

    if amount <= 0:
        return False, "Invalid Amount"

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_no=%s
        """,
        (amount, acc_no)
    )

    conn.commit()

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (acc_no,)
    )

    balance = cursor.fetchone()["balance"]

    return True, f"Deposit Successful. Current Balance: ₹{balance:.2f}"


from decimal import Decimal

def do_withdraw(acc_no, amount):

    amount = Decimal(str(amount))

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (acc_no,)
    )

    balance = cursor.fetchone()["balance"]

    if amount <= 0:
        return False, "Invalid Amount"

    if amount > balance:
        return False, "Insufficient Balance"

    cursor.execute(
        "UPDATE accounts SET balance = balance - %s WHERE account_no=%s",
        (amount, acc_no)
    )

    conn.commit()

    return True, f"Withdrawal Successful. Current Balance: ₹{balance - amount:.2f}"


def do_transfer(sender, receiver, amount):

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (sender,)
    )

    sender_balance = cursor.fetchone()["balance"]

    if amount > sender_balance:
        return False, "Insufficient Balance"

    cursor.execute(
        "SELECT * FROM accounts WHERE account_no=%s",
        (receiver,)
    )

    if cursor.fetchone() is None:
        return False, "Receiver Account Not Found"

    cursor.execute(
        "UPDATE accounts SET balance=balance-%s WHERE account_no=%s",
        (amount, sender)
    )

    cursor.execute(
        "UPDATE accounts SET balance=balance+%s WHERE account_no=%s",
        (amount, receiver)
    )

    conn.commit()

    return True, "Transfer Successful"


def do_change_password(acc_no, old_pw, new_pw):

    cursor.execute(
        """
        SELECT password
        FROM accounts
        WHERE account_no=%s
        """,
        (acc_no,)
    )

    password = cursor.fetchone()["password"]

    if password != old_pw:
        return False, "Wrong Password"

    cursor.execute(
        """
        UPDATE accounts
        SET password=%s
        WHERE account_no=%s
        """,
        (new_pw, acc_no)
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
            else:
                acc_no = create_account(name.strip(), int(age), mobile.strip(), password)
                st.success("Account Created Successfully!")
                st.info(f"Your Account Number is **{acc_no}** — save it, you'll need it to log in.")

#customer Menu

def show_customer_dashboard():
    acc = st.session_state.logged_in_acc
    
    cursor.execute(
    "SELECT * FROM accounts WHERE account_no=%s",
    (acc,)
    )

    info = cursor.fetchone()

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
        cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=%s",
        (acc,)
        )

        balance = cursor.fetchone()["balance"]

        st.metric("Balance", f"₹{balance:.2f}")

    elif menu == "Deposit Money":
        st.subheader("Deposit Money")
        with st.form("deposit_form"):
            amount = st.number_input("Enter Deposit Amount", min_value=0.0, step=100.0)
            submitted = st.form_submit_button("Deposit")
        if submitted:
            ok, msg = do_deposit(acc, amount)
            (st.success if ok else st.error)(msg)

    elif menu == "Withdraw Money":
        st.subheader("Withdraw Money")
        with st.form("withdraw_form"):
            amount = st.number_input("Enter Withdraw Amount", min_value=0.0, step=100.0)
            submitted = st.form_submit_button("Withdraw")
        if submitted:
            ok, msg = do_withdraw(acc, amount)
            (st.success if ok else st.error)(msg)

    elif menu == "Transfer Money":
        st.subheader("Transfer Money")
        with st.form("transfer_form"):
            receiver = st.text_input("Enter Receiver Account Number")
            amount = st.number_input("Enter Amount", min_value=0.0, step=100.0)
            submitted = st.form_submit_button("Transfer")
        if submitted:
            if not receiver.strip().isdigit():
                st.error("Please enter a valid numeric account number.")
            else:
                ok, msg = do_transfer(acc, int(receiver), amount)
                (st.success if ok else st.error)(msg)

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
            ok, msg = do_change_password(acc, old_pw, new_pw)
            (st.success if ok else st.error)(msg)

    elif menu == "Logout":
        st.session_state.logged_in_acc = None
        st.success("Logged Out Successfully")
        st.rerun()



#replaces the while True: menu loop

if st.session_state.logged_in_acc is None:
    show_auth_screen()
else:
    show_customer_dashboard()
