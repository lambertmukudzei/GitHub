#This is my Main login/registration page for the application
import streamlit as st
import bcrypt
import sqlite3
import pandas as pd  # Added missing import
from pathlib import Path

# We start off with the page configuration
st.set_page_config(
    page_title="Intelligence Platform - Login",
    page_icon="🔐",
    layout="centered"
)

#Database Functions
def connect_db():
    """Connecting to my Week 8 database"""
    db_path = Path("DATA") / "intelligence_platform.db"
    return sqlite3.connect(str(db_path))

def verify_password(username, password):
    """Verify password using Week 7 bcrypt - FIXED version"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            stored_hash = user[2]  # password_hash column
            password_bytes = password.encode('utf-8')
            hash_bytes = stored_hash.encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, hash_bytes):
                return True, user
        return False, None
    except Exception as e:
        st.error(f"Database error: {e}")
        return False, None

def check_user_exists(username):
    #Checks if a user exists in our database"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except Exception as e:
        st.error(f"Error checking user: {e}")
        return False

def register_user_in_db(username, password, role="user"):
    #Register a new user using my Week 7 and Week 8 code
    try:
        # Hashing password with bcrypt from Week 7
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        password_hash = hashed.decode('utf-8')
        
        # Insert into database (Week 8)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        conn.close()
        return True, "Registration was successful!"
    except sqlite3.IntegrityError:
        return False, "Sorry Username already exists."
    except Exception as e:
        return False, f"Error: {str(e)}"

#Initialize Session State
# This stores login info across multiple pages
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = ""

#Page Title
st.title("🔐 Multi-Domain Intelligence Platform")
st.write("Welcome user! Please login or register to access the dashboard.")

# we now Check if Already Logged In
if st.session_state.logged_in:
    st.success(f"✅ Already logged in as **{st.session_state.username}** ({st.session_state.user_role})")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Dashboard", type="primary"):
            st.switch_page("pages/1_Dashboard.py")
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.rerun()  # Refresh the page
    
    st.stop()  # Don't show login/register forms

#Login/Register Tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

#LOGIN TAB
with tab_login:
    st.subheader("Login to Your Account")
    
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Login", type="primary", use_container_width=True):
            if login_username and login_password:
                # Verify credentials using Week 7 authentication
                is_valid, user = verify_password(login_username, login_password)
                
                if is_valid:
                    # Set session state
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    # Get user role (column index 3) or default to "user"
                    st.session_state.user_role = user[3] if user and len(user) > 3 else "user"
                    
                    st.success(f"Welcome back, {login_username}! 🎉")
                    st.balloons()
                    
                    # Redirect to dashboard
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please enter both username and password.")
    
    with col2:
        # Demo credentials button
        if st.button("Use Demo", help="Try with demo credentials"):
            st.info("Try: Username: test_user, Password: SecurePass123!")

#REGISTER TAB
with tab_register:
    st.subheader("Create a New Account")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    # Password strength check (from Week 7)
    st.caption("Password requirements: 6+ characters, uppercase, lowercase, number")
    
    if st.button("Create Account", type="primary"):
        # Basic Input  validation
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif len(new_username) < 3:
            st.error("Username must be at least 3 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            # Check password strength (Week 7 logic)
            has_upper = any(char.isupper() for char in new_password)
            has_lower = any(char.islower() for char in new_password)
            has_digit = any(char.isdigit() for char in new_password)
            
            if not (has_upper and has_lower and has_digit):
                st.error("Password must contain uppercase, lowercase, and number.")
            else:
                # Register user in database
                success, message = register_user_in_db(new_username, new_password)
                
                if success:
                    st.success("✅Congratulations, Account created successfully!")
                    st.info("Please Switch to the Login tab to sign in with your new account.")
                    
                    # Show existing users from database
                    try:
                        conn = connect_db()
                        users_df = pd.read_sql_query("SELECT username, role FROM users", conn)
                        conn.close()
                        
                        st.subheader("Current Users in System")
                        st.dataframe(users_df, use_container_width=True)
                    except Exception as e:
                        st.write(f"Note: Could not load users - {e}")
                else:
                    st.error(f"Registration failed: {message}")

#Footer
st.divider()
st.caption("🔐 This uses the secure authentication system from Week 7")
st.caption("🗄️ User data is stored in the SQLite database from Week 8")