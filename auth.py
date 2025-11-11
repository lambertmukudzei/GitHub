import bcrypt
import os

def hash_password(password):
    #Turn a plain text password into a secure hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password, hashed):
    #Check if a password matches the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register():
    #Create a new user account
    print("\n--- Registration ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/user): ")
    
    hashed_password = hash_password(password)
    
    with open("users.txt", "a") as file:
        file.write(f"{username},{hashed_password.decode('utf-8')},{role}\n")
    
    print("Registration successful!")

def login():
    #Verify user login credentials
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    try:
        with open("users.txt", "r") as file:
            for line in file:
                stored_username, stored_hash, role = line.strip().split(",")
                
                if stored_username == username:
                    if verify_password(password, stored_hash.encode('utf-8')):
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

def main():
    # My Main program loop
    while True:
        print("\n=== Simple Auth System ===")
        print("1. Register")
        print("2. Login") 
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
