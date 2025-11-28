# reset_database.py
import os
from pathlib import Path

def reset_database():
    db_path = Path("DATA/intelligence_platform.db")
    if db_path.exists():
        os.remove(db_path)
        print("Old database deleted")
    
    # Recreate DATA folder
    Path("DATA").mkdir(exist_ok=True)
    print("Database reset complete - ready for fresh setup")

if __name__ == "__main__":
    reset_database()
