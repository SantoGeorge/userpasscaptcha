import sqlite3
import hashlib
import random
import string
import datetime

#DATABASE CONNECTION 
conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

#USER REGISTRATION 
username = input("Enter Username: ")

# Password validation loop
while True:

    password = input("Enter Password: ")

    upper = False
    lower = False
    digit = False
    symbol = False
    space = False

    for ch in password:
        if ch.isupper():
            upper = True

        elif ch.islower():
            lower = True

        elif ch.isdigit():
            digit = True

        elif ch.isspace():
            space = True

        else:
            symbol = True

    # Password Conditions
    if len(password) < 8:
        print("Weak Password - Must contain at least 8 characters")

    elif not password[0].isalpha():
        print("Weak Password - Must start with an alphabet")

    elif not upper:
        print("Weak Password - Must contain an uppercase letter")

    elif not lower:
        print("Weak Password - Must contain a lowercase letter")

    elif not digit:
        print("Weak Password - Must contain a digit")

    elif not symbol:
        print("Weak Password - Must contain a symbol")

    elif space:
        print("Weak Password - Should not contain spaces")

    else:
        print("Strong Password")
        break

#STORE USERNAME AND PASSWORD
hashed_password = hashlib.sha256(password.encode()).hexdigest()

cur.execute(
    "INSERT INTO users VALUES(?, ?)",
    (username, hashed_password)
)

conn.commit()

# LOGIN SECTION 
print("\n LOGIN ")

login_username = input("Re-enter Username: ")
login_password = input("Re-enter Password: ")

hashed_login_password = hashlib.sha256(
    login_password.encode()
).hexdigest()

# Check username and password
cur.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (login_username, hashed_login_password)
)

result = cur.fetchone()

# CAPTCHA SECTION 
if result:

    captcha = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )

    print("\nCaptcha:", captcha)

    user_captcha = input("Enter Captcha: ")

    if user_captcha == captcha:

        print("\nLogin Successful")

        now = datetime.datetime.now()

        # Write login details into text file
        with open("login_details.txt", "a") as f:

            f.write("\nLOGIN SUCCESSFUL\n")
            f.write("Username : " + login_username + "\n")
            f.write("Date     : " + str(now.date()) + "\n")
            f.write("Time     : " + str(now.time()) + "\n")

    else:
        print("\nIncorrect Captcha")

        now = datetime.datetime.now()

        with open("login_details.txt", "a") as f:

            f.write("\n LOGIN FAILED\n")
            f.write("Reason   : Incorrect Captcha\n")
            f.write("Username : " + login_username + "\n")
            f.write("Date     : " + str(now.date()) + "\n")
            f.write("Time     : " + str(now.time()) + "\n")

else:

    print("\nInvalid Username or Password")

    now = datetime.datetime.now()

    with open("login_details.txt", "a") as f:

        f.write("\nLOGIN FAILED \n")
        f.write("Reason   : Invalid Username or Password\n")
        f.write("Username : " + login_username + "\n")
        f.write("Date     : " + str(now.date()) + "\n")
        f.write("Time     : " + str(now.time()) + "\n")

# ---------------- CLOSE DATABASE ----------------
conn.close()