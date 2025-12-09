# This file handles user registration, login, and data migration
import bcrypt  # For encrypting passwords
import sqlite3  # For database operations
from pathlib import Path  # For working with file paths
from app.data.db import connect_database  # My database connection function
from app.data.users import get_user_by_username, insert_user  # User database functions

def register_user(username, password, role="user"):
    """Register a new user - create account"""
    # Now WE CAN Check if a user already exists
    if get_user_by_username(username):
        return False, f"Username '{username}' already exists."
    
    # Hash the password (convert to secret code)
    password_bytes = password.encode('utf-8')  # Convert string to bytes
    salt = bcrypt.gensalt()  # Add random salt for security
    hashed = bcrypt.hashpw(password_bytes, salt)  # Create encrypted hash
    password_hash = hashed.decode('utf-8')  # Convert back to string
    
    # here we can Insert a new user into database
    try:
        insert_user(username, password_hash, role)
        return True, f"User '{username}' registered successfully!"
    except sqlite3.Error as e:
        return False, f"Registration failed: {e}"

def login_user(username, password):
    """Check username and password - login"""
    # Get user from database
    user = get_user_by_username(username)
    
    if not user:  # User doesn't exist
        return False, "Username not found."
    
    # Verify password (user[2] is password_hash column in database)
    stored_hash = user[2]  # Get stored encrypted password
    password_bytes = password.encode('utf-8')  # Convert entered password
    hash_bytes = stored_hash.encode('utf-8')  # Convert stored hash
    
    # Compare entered password with stored hash
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Move users from text file to database"""
    filepath = Path(filepath)  # Convert to Path object
    
    # Check if file exists
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return 0  # Return 0 migrated users
    
    # Connect to database
    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0  # Count successful migrations
    
    # Open and read the text file
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()  # Remove whitespace
            if not line:  # Skip empty lines
                continue
            
            # Parse line: username,password_hash (comma separated)
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                
                # Insert user into database (skip if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:  # If a row was inserted
                        migrated_count += 1
                        print(f"   Migrated user: {username}")
                except sqlite3.Error as e:
                    print(f" Error migrating user {username}: {e}")
    
    # Save changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Migrated {migrated_count} users from {filepath.name}")
    return migrated_count  # Return how many users were migrated