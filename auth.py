import bcrypt
import os
from getpass import getpass
import re

USER_DATA_FILE = "users.txt"

def hash_password(password):
    #Turn a plain text password into a secure hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    #Check if a password matches the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def user_exists(username):
    #Check if username already exists
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    try:
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                if line.strip():
                    stored_username = line.split(',')[0]
                    if stored_username == username:
                        return True
    except FileNotFoundError:
        return False
    
    return False

def validate_username(username):
    #Check if username meets requirements
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""

def validate_password(password):
    #Check if password is strong enough
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password must be no more than 50 characters long."
    
    # Make it a bit stronger
    if not any(char.isupper() for char in password):
        return False, "Password should contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password should contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return False, "Password should contain at least one digit."
    
    return True, ""

def register():
    #Create a new user account
    print("\n--- Registration ---")
    username = input("Enter username: ").strip()
    
    # This will check if a user exists
    if user_exists(username):
        print("Error: Username already exists!")
        return
    
    #We will apply Input validation here
    is_valid, error_msg = validate_username(username)
    if not is_valid:
        print(f"Error: {error_msg}")
        return
    
    #Here we will use getpass to hide password input
    password = getpass("Enter password: ").strip()
    
    #Here we will validate whether the password is strong enough
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        print(f"Error: {error_msg}")
        return
    
    # We will confirm the password
    password_confirm = getpass("Confirm password: ").strip()
    if password != password_confirm:
        print("Error: Passwords do not match!")
        return
    
    role = input("Enter role (admin/user): ").strip().lower()
    if role not in ['admin', 'user']:
        print("Error: Role must be 'admin' or 'user'")
        return
    
    hashed_password = hash_password(password)
    
    with open("users.txt", "a") as file:
        file.write(f"{username},{hashed_password},{role}\n")
    
    print("Registration successful!")

def login():
    #Verify user login credentials
    print("\n--- Login ---")
    username = input("Enter username: ").strip()
    password = getpass("Enter password: ").strip()
    
    try:
        with open("users.txt", "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        stored_username, stored_hash, role = parts
                        
                        if stored_username == username:
                            if verify_password(password, stored_hash):
                                print(f"Login successful! Welcome {username} ({role})")
                                return True
                            else:
                                print("Invalid password!")
                                return False
            
        print("Username not found!")
        return False
        
    except FileNotFoundError:
        print("No users registered yet!")
        return False

def display_menu():
    #We will create a formatted menu
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    # My Main program loop
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

#Now we will create some test functions
def test_hashing():
    #I will now test the hashing functions
    print("=== Testing Hashing Functions ===")
    test_password = "SecurePassword123"
    
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}")
    print(f"Hash length: {len(hashed)} characters")
    
    # this is Test for the correct password
    is_valid = verify_password(test_password, hashed)
    print(f"Correct password test: {is_valid}")
    
    # This will Test for wrong password
    is_invalid = verify_password("WrongPassword", hashed)
    print(f"Wrong password test: {is_invalid}")

if __name__ == "__main__":
    
    # Now we will Run the main program
    main()
