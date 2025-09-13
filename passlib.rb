from passlib.hash import bcrypt

# Replace with the hash from the database
stored_hash = "$2b$12$luXEn.4hxyRPMCcegYDD6.wAKG8pP.4HLxCTxP89ElLlpxinKi3dG"

# Replace with the password you want to test
password_to_test = "admin123"

# Verify the password
if bcrypt.verify(password_to_test, stored_hash):
    print("Password is correct!")
else:
    print("Password is incorrect!")