import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

def register_user(username, password, role="user"):
    """Register a new user."""
    # Now WE CAN Check if a user already exists
    if get_user_by_username(username):
        return False, f"Username '{username}' already exists."
    
    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')
    
    # here we can Insert a new user
    try:
        insert_user(username, password_hash, role)
        return True, f"User '{username}' registered successfully!"
    except sqlite3.Error as e:
        return False, f"Registration failed: {e}"

def login_user(username, password):
    """Authenticate a user."""
    user = get_user_by_username(username)
    
    if not user:
        return False, "Username not found."
    
    # Verify password (user[2] is password_hash column)
    stored_hash = user[2]
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        return 0
    
    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                
                # Insert  a user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                        print(f"   Migrated user: {username}")
                except sqlite3.Error as e:
                    print(f"❌ Error migrating user {username}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")
    return migrated_count
