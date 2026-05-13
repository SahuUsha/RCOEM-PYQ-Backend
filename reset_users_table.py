import sys
import os

# Add the current directory to sys.path to import app modules
sys.path.append(os.getcwd())

from app.database import engine, Base
from app.models import User
from sqlalchemy import text

def reset_users():
    print("Dropping and recreating the 'users' table...")
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
            conn.commit()
            print("Dropped existing 'users' table.")
        
        # This will create all tables that don't exist, including the 'users' table we just dropped
        Base.metadata.create_all(bind=engine)
        print("Successfully recreated the 'users' table with the correct schema.")
    except Exception as e:
        print(f"Error resetting users table: {e}")

if __name__ == "__main__":
    reset_users()
