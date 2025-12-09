# This handles user login and registration it's like a security guard for the app
import bcrypt  # Library for encrypting passwords
from typing import Optional, Tuple
from models.user import User  # My User class
from services.database_manager import DatabaseManager  # Database connection
import sqlite3  # Database library

class AuthManager:
    # Handles user registration and login - the login system
    
    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager  # Connect to database
    
    def register_user(self, username: str, password: str, role: str = "user") -> Tuple[bool, str]:
        #Create new user account
        try:
            # Step 1: Hash password (convert to unreadable secret code)
            password_bytes = password.encode('utf-8')  # Convert to bytes
            salt = bcrypt.gensalt()  # Add random salt (extra security)
            hashed = bcrypt.hashpw(password_bytes, salt)  # Create hash
            password_hash = hashed.decode('utf-8')  # Convert back to string
            
            # Step 2: Save to database
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            return True, "Registration successful!"  # Success message
            
        except sqlite3.IntegrityError:  # Username already exists
            return False, "Username already exists."
        except Exception as e:  # Any other error
            return False, f"Error: {str(e)}"
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        """Check if username and password are correct"""
        # Step 1: Get user from database
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        
        if row is None:  # User doesn't exist
            return None
        
        username_db, password_hash_db, role_db = row  # Unpack database row
        
        # Step 2: Check password
        password_bytes = password.encode('utf-8')  # Convert entered password
        hash_bytes = password_hash_db.encode('utf-8')  # Convert stored hash
        
        # Compare entered password with stored hash
        if bcrypt.checkpw(password_bytes, hash_bytes):
            return User(username_db, password_hash_db, role_db)  # Login successful
        
        return None  # Wrong password
    
    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        # Compare password with hash
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)  # Returns True/False