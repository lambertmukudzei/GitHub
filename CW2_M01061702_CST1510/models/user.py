# This is my User class, it stores information about each user
#student ID: M01061702
class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""
    
    def __init__(self, username: str, password_hash: str, role: str):
        # These are PRIVATE attributes (start with __)
        # They can't be accessed directly from outside the class
        self.__username = username  # User's login name
        self.__password_hash = password_hash  # Encrypted password (not the real password)
        self.__role = role  # User's role like "user", "admin", etc.
    
    def get_username(self) -> str:
        """Get the username"""
        return self.__username  # Returns the username
    
    def get_password_hash(self) -> str:
        """Get the password hash (encrypted password)"""
        return self.__password_hash  # Returns the hashed password
    
    def get_role(self) -> str:
        """Get the user's role"""
        return self.__role  # Returns the user's role
    
    def verify_password(self, plain_password: str, hasher) -> bool:
        """Check if a plain-text password matches this user's hash."""
        # Compares the entered password with the stored hash
        return hasher.check_password(plain_password, self.__password_hash)
    
    def __str__(self) -> str:
        """String representation of the user (for printing)"""
        return f"User({self.__username}, role={self.__role})"