import bcrypt
import os

# File where we store user data
USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    # This function takes a plain text password and makes it secure by hashing
    # Hashing is like scrambling the password so it can't be read
    
    # First, convert the password to bytes because bcrypt needs bytes
    password_bytes = plain_text_password.encode('utf-8')
    
    # Generate a salt - this is like adding extra random stuff to make each hash unique
    salt = bcrypt.gensalt()
    
    # Create the hash by combining the password and salt
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Convert the hash back to a string so we can store it in a file
    hashed_password = hashed_bytes.decode('utf-8')
    
    return hashed_password

def verify_password(plain_text_password, hashed_password):
    # This function checks if a password matches the stored hash
    
    # Convert both to bytes for bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Use bcrypt to check if they match
    # bcrypt is smart - it knows how to extract the salt from the hash
    if bcrypt.checkpw(password_bytes, hashed_bytes):
        return True
    else:
        return False

def user_exists(username):
    # Check if a username is already taken
    
    # First check if the users file even exists
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    # Read the file and look for the username
    try:
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 1 and parts[0] == username:
                    return True
    except:
        return False
    
    return False

def register_user(username, password):
    # Register a new user account
    
    # Check if username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    # Hash the password for security
    hashed_pw = hash_password(password)
    
    # Save the username and hashed password to file
    try:
        with open(USER_DATA_FILE, 'a') as file:
            file.write(f"{username},{hashed_pw}\n")
        print(f"Success: User '{username}' registered successfully!")
        return True
    except Exception as e:
        print(f"Error saving user: {e}")
        return False

def login_user(username, password):
    # Log in a user by checking their username and password
    
    # Check if any users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False
    
    # Look for the username in the file
    try:
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[0] == username:
                    # Found the user, now check if password is correct
                    stored_hash = parts[1]
                    if verify_password(password, stored_hash):
                        print(f"Success: Welcome, {username}!")
                        return True
                    else:
                        print("Error: Invalid password.")
                        return False
    except:
        print("Error: User database not found.")
        return False
    
    # If we get here, the username wasn't found
    print("Error: Username not found.")
    return False

def validate_username(username):
    # Check if username meets requirements
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    
    # Check if only letters and numbers
    if not username.isalnum():
        return False, "Username can only contain letters and numbers."
    
    return True, ""

def validate_password(password):
    # Check if password is strong enough
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    if len(password) > 50:
        return False, "Password must be no more than 50 characters long."
    
    # Check for different types of characters
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain at least one uppercase letter, one lowercase letter, and one number."
    
    return True, ""

def display_menu():
    # Show the main menu
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    # This is the main program that runs everything
    print("\nWelcome to the Week 7 Authentication System!")
    
    # Create users file if it doesn't exist
    if not os.path.exists(USER_DATA_FILE):
        open(USER_DATA_FILE, 'a').close()
    
    # Main program loop - keeps running until user chooses to exit
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # User wants to register
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Check if username is valid
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
            # Check if password is strong enough
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Ask user to type password again to confirm
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Try to register the user
            register_user(username, password)
            
        elif choice == '2':
            # User wants to login
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Try to login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the database)")
                
                # Wait for user to press enter before continuing
                input("\nPress Enter to return to main menu...")
            
        elif choice == '3':
            # User wants to exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

# This runs when we start the program
if __name__ == "__main__":
    main()