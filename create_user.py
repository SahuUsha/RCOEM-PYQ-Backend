import sys
import os

# Add the current directory to sys.path to import app modules
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models import User
from app.services.auth_service import get_password_hash
import getpass

def create_user():
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match!")
        return

    hashed_password = get_password_hash(password)
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists!")
            return

        new_user = User(email=email, password=hashed_password)
        db.add(new_user)
        db.commit()
        print(f"User {email} created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_user()
