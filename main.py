# this is for user registration.
users={}
next_user=100

name=input("Enter your Full Name: ")
mobile_no=int(input("enter the mobile_no.:"))
password=input("enter the password:")

users[next_user]={
    "name":name,"mob_no":mobile_no,"pswd":password}
next_user+=1
print("User Registered Successfully")
    
    