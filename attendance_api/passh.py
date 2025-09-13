from passlib.hash import argon2

new_password = "admin123"
hashed_password = argon2.hash(new_password)
print(f"Hashed password: {hashed_password}")
