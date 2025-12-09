# My 1_Login.py
#Student ID: M01061702
#Now we import the libraries we need such as streamlit, sys, time and our custom managers
import streamlit as st
import sys
import time
# Importing our custom modules - these are the files I created in the services folder
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

#we start off by configuring the Page
st.set_page_config(
    page_title="Login -CST1510 Intelligence Platform",
    page_icon="🔐",
    layout="centered"
)
# FIXING A STREAMLIT PROBLEM
# Streamlit 1.24.0 had a bug where st.rerun() didn't work properly
# So I had to find another way to refresh the page
# I learned about JavaScript refresh from ChatGPT
def refresh_page():
    """Refresh the page using JavaScript - my workaround for the bug"""
    # JavaScript is another programming language that runs in browsers
    st.markdown('<script>window.location.reload();</script>', unsafe_allow_html=True)
    time.sleep(0.1) # Waits for a bit
    st.stop()#Stops streamlit from running further 
# Check if st.rerun exists (it might not in older versions)
if not hasattr(st, 'rerun') or not callable(getattr(st, 'rerun', None)):
    st.rerun = refresh_page
    print("Using JavaScript page refresh for st.rerun()", file=sys.stderr)
#End of JavaScript Refresh

# Here we intialize managers
# INITIALIZING - setting things up
# @st.cache_resource means Streamlit will remember these and not reload them every time
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

@st.cache_resource  
def get_auth_manager():
    return AuthManager(get_db_manager())# Creating database manager 
# Actually creating the managers we'll use
db_manager = get_db_manager()
auth_manager = get_auth_manager()# Creating authentication manager using my database manager

#Now we must Check if the user already logged in
# Session state is like memory that stays while you use the app
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.switch_page("pages/2_Cyber_Security.py")

# Page Title
st.title("CST1510 Multi Domain Intelligence Platform")
st.write("Good Day! Please login or register to access this CST1510 Intelligence platform.")

# Login/Register Tabs
# Creating tabs FOR LOGIN AND REGISTER
# Like having two different pages in one
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login to Your Account here")
    
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
     # When login button is clicked
    if st.button("Login", type="primary"):
        if login_username and login_password:
            user = auth_manager.login_user(login_username, login_password)
            
            if user:  #If login is successful
                #We Save the user info in session state (memory)
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.user_role = user.get_role()
                st.session_state.current_user = user
                
                st.success(f"We are pleased to Welcome you back, {user.get_username()}! 🎉")
                st.balloons()# Show success message with balloons!-I added this to add a flair to the app
                st.switch_page("pages/2_Cyber_Security.py")
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both the username and password")
    
    if st.button("Use Demo"):
        st.info("Try: Username: test_user, Password: SecurePass123!")

with tab_register:
    st.subheader("Create a New Account here")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    if st.button("Create Account", type="primary"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            success, message = auth_manager.register_user(new_username, new_password)
            
            if success:
                st.success("Well Done. Account created successfully!")
                st.info("Please login with your new account.")
            else:
                st.error(f"Soory Registration failed: {message}")

# Footer
st.divider()
st.caption("CST1510 Multi Domain Intelligence Platform - Login Page")