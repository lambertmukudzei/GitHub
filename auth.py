import bcrypt
import os
import re

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password): 
    """
    Hashes a password using bcrypt with automatic salt generation.
    
    Args:
        plain_text_password (str): The plaintext password to hash
    
    Returns:
        str: The hashed password as a UTF-8 string
    """
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    # Hashing the password with the generated salt
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Decoding the hash back into a string 
    hashed_password = hashed_bytes.decode('utf-8')
    return hashed_password

def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plaintext password against a hashed password.
    
    Args: 
        plain_text_password (str): The plaintext password to verify
        hashed_password (str): The hashed password to verify against
    Returns: 
        bool: True if the password matches, False otherwise
    """
    # We are now converting the plaintext password and the stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Using bcrypt's checkpw function to verify the password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def user_exists(username):
    """
    Checks if a user exists in the user data file.
    
    Args:
        username (str): The username to check
    """
    # We need to handle the case where the user data file might not exist yet
    if not os.path.isfile(USER_DATA_FILE):
        return False
    # We need to read the user data file and check for the username  
    try:          
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                if line.strip():
                    stored_username = line.split(',')[0].strip()
                    if stored_username == username:
                        return True
    except FileNotFoundError:
        return False
    
    return False

def register_user(username, plain_text_password):
    """
    Registers a new user by storing their username and hashed password.
    
    Args:
        username (str): The username of the new user
        plain_text_password (str): The password to register
    """
    # Check if the user already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    # Hash the user's password
    hashed_password = hash_password(plain_text_password)
    # Append the new user's data to the user data file
    # format is username,hashed_password
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{hashed_password}\n")
    print(f"Success: User '{username}' registered.")
    return True

def login_user(username, plain_text_password):
    """
    Authenticates a user by verifying their username and password.
    
    Args:
        username (str): The username of the user
        plain_text_password (str): The password to verify
    """
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False
    # We need to search for the username in the user data file
    try:
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        stored_username = parts[0].strip()
                        stored_hashed_password = parts[1].strip()
                        if stored_username == username:
                            if verify_password(plain_text_password, stored_hashed_password):
                                print(f"Success: Welcome, {username}!")
                                return True
                            else:
                                print("Error: Invalid password.")
                                return False
    except FileNotFoundError:
        print("Error: User database not found.")
        return False
    
    # If we reach here, the username was not found
    print("Error: Username not found.")
    return False

# Input Validation Functions
def validate_username(username):
    """
    Validates username format.
    
    Args:
        username (str): The username to validate
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""

def validate_password(password):
    """
    Validates password strength.
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password must be no more than 50 characters long."
    
    # Check for password strength (optional enhancement)
    if check_password_strength(password) == "Weak":
        return False, "Password is too weak. Include uppercase, lowercase, numbers, and special characters."
    
    return True, ""

def check_password_strength(password):
    """
    Checks the strength of a password.
    
    Args:
        password (str): The password to check
    
    Returns:
        str: "Weak", "Moderate", or "Strong"
    """
    score = 0
    
    # Length check
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    
    # Character variety checks
    if re.search(r"[A-Z]", password):  # Uppercase
        score += 1
    if re.search(r"[a-z]", password):  # Lowercase
        score += 1
    if re.search(r"\d", password):     # Digits
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Special characters
        score += 1
    
    if score >= 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"

# Main Menu and Program Logic
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("MY MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """My Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard)")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

# Test Functions (Temporary - remove after testing)
def test_hashing_functions():
    """Test the hashing and verification functions."""
    print("=== TESTING HASHING FUNCTIONS ===")
    test_password = "SecurePassword123"
    
    # Test hashing
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}")
    print(f"Hash length: {len(hashed)} characters")
    
    # Test verification with correct password
    is_valid = verify_password(test_password, hashed)
    print(f"\nVerification with correct password: {is_valid}")
    
    # Test verification with incorrect password
    is_invalid = verify_password("WrongPassword", hashed)
    print(f"Verification with incorrect password: {is_invalid}")

if __name__ == "__main__":
    # test_hashing_functions()
    
    main()