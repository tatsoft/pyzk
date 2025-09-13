from passlib.hash import bcrypt

new_password = "new_admin_password"
hashed_password = bcrypt.hash(new_password)
print(hashed_password)