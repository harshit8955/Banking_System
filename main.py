# this is for user registration.

accounts={}
def create_account():
    print("---Create New Account---")
    name=(input("Enter your full name:"))
    mobile_no=int(input("Enter your mobile number:"))
    password=input("Enter the password:")
    
    intial_deposite=float(input("Enter the amount you want to deposite:"))
    
    if intial_deposite<0:
        print("Amount can't be negetive:")
        return    
    New_account_no. = 100+len(accounts)
    accounts[New_account_number]={
        "name":name,
        "password":password,
        "current balance":intial_deposite
    }
    print("Account created successfully! Your account number is {New_account_number}")
    print("Please save this number, you'll need it to log in.")


# users login function.

