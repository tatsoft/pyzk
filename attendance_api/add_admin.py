"""Module providing a function printing python version."""

import sys
import os
from attendance_api.database import SessionLocal
from attendance_api.models import Employee
from attendance_api.auth import get_password_hash

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
# Define the new admin user details
new_admin = {
    "name": "New Admin",
    "code": "admin2",
    "department": "Administration",
    "password_hash": get_password_hash("admin123"),  # Replace with the desired password
    "is_admin": True
}

# Add the new admin user to the database
def add_admin():
    with SessionLocal() as session:
        # Check if the admin already exists
        existing_admin = session.query(Employee).filter(Employee.code == new_admin["code"]).first()
        if existing_admin:
            print("Admin user already exists!")
            return

        # Create and add the new admin
        admin = Employee(**new_admin)
        session.add(admin)
        session.commit()
        print("New admin user added successfully!")

if __name__ == "__main__":
    add_admin()