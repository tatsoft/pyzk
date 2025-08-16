# Script to add an admin user to the database for FastAPI backend
from attendance_api.database import SessionLocal
from attendance_api.models import Employee
from attendance_api.auth import get_password_hash


def create_admin():
    db = SessionLocal()
    code = "admin"
    password = "admin"  # Change this to a secure password if needed
    name = "Admin"
    is_admin = True
    # Check if admin already exists
    existing = db.query(Employee).filter(Employee.code == code).first()
    if existing:
        print("Admin user already exists.")
        db.close()
        return
    admin = Employee(
        code=code,
        name=name,
        password_hash=get_password_hash(password),
        is_admin=is_admin
    )
    db.add(admin)
    db.commit()
    db.close()
    print("Admin user created: code='admin', password='admin'")

if __name__ == "__main__":
    create_admin()
