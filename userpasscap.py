import sqlite3
import hashlib
import datetime
import random
import string
# Connect to database
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")
cur.execute("DELETE FROM users")
username=input("enter the user name ")
password=input("enter the password")
upper=False
lower=False
space=False
symbol=False
digit=False
ar=0
for s in password:
    if s.isupper()==True:
        upper=True
    elif s.islower()==True :
        lower=True
    elif s.isdigit()==True:
        digit=True
    elif s.isspace==True:
        space=True
    else:
        symbol=True
if password[0].isalpha()==False:
    print("password must start with alphabets")
    password=input("enter correct form  password")
    exit()
for  a in password:
    if a==ar:
        print("not possible")
        exit()
    else:
        ar=a

if len(password)<8:
    print(" weak password ,password atleast contain only 8 character ") 
    password=input("enter correct form  password")
elif not upper:
    print("weak password,password contain uppercase letter")
    password=input("enter correct form  password")
elif not  lower:
    print("weak password,password contain atlest one lowercase")
    password=input("enter correct form  password")
elif not  digit:
    print("weak password ,password contain atleast one digit")
    password=input("enter correct form  password")
elif   space:
    print("weak password,password not contain any space")
    password=input("enter correct form  password")
elif not  symbol:
    print("weak password,password not contain any symbol")
    password=input("enter correct form  password")
else:
    print("strong password") 
hashpas=hashlib.sha256(password.encode())
hashed=hashpas.hexdigest()
cur.execute("INSERT INTO users VALUES(?, ?)", (username, hashed))
conn.commit()
newusername = input("Enter username: ")
newpassword = input("Enter password: ")
hashpasd=hashlib.sha256(newpassword.encode())
nhashed=hashpasd.hexdigest()

# Secure query using parameterized statements
cur.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (newusername, nhashed)
)
result = cur.fetchone()
captcha = ''.join(random.choices(
    string.ascii_letters + string.digits, k=6))
attempts = 3
while attempts>0:
    print("\nCaptcha:", captcha)
    user_input = input("Enter the captcha: ")
# Check login
    if result and user_input==captcha:
        print("login sucess")
        with open("file1.txt","a") as f:
            now=str(datetime.datetime.now())
            f.write("\n")
            f.write("\n")
            f.write("login sucess")
            f.write("\n")
            f.write("USERNAME:")
            f.write(newusername)
            f.write("\n")
            f.write("DATE AND TIME:")
            f.write(now)
            f.write("\n")

        break    
    
    else:
        attempts -= 1
        print(" Wrong Captcha")
        if attempts > 0:
            print("Remaining Attempts:", attempts)
        else:
            print(" Login Failed")
# Close connection
conn.close()
