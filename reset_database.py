from app.data.db import connect_database
from pathlib import Path

def reset_database():
    print("Resetting database...")
    
    # Delete existing database file
    db_path = Path("DATA/intelligence_platform.db")
    if db_path.exists():
        db_path.unlink()
        print("Deleted old database")
    
    # Recreate with correct schema
    conn = connect_database()
    from app.data.schema import create_all_tables
    create_all_tables(conn)
    conn.close()
    print("Database reset with correct schema")

if __name__ == "__main__":
    reset_database()