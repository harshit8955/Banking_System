# this is for user registration.
users={}
next_user=100

name=input("Enter your Full Name: ")
mobile_no=int(input("enter the mobile_no.:"))
password=input("enter the password:")

users[next_user]={
    "name":name,"mob_no":mobile_no,"pswd":password,"balance":0}
next_user+=1
print("User Registered Successfully")


# users login function.

def login():
    print("\n------------login----------")
    acc=int(input("enter your account number:"))
    
    password=input("enter your password:")
    if acc in users:
        if users[acc]["pswd"]==password:
            print("user is verified")
            print("users Name:",name,",it is your account number:",next_user)
            print("Mobile number:",mobile_no)
        else:
            print("user is faltu")
    else:
        print("faltu users account no. is not valid.")
            

login()