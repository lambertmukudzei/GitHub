# Home.py - This is the main landing page of my application
# Student ID: M01061702

# Import the main library for creating web apps
import streamlit as st

# Configure the page settings
st.set_page_config(
    page_title="CST1510 Intelligence Platform",  # What appears in browser tab
    page_icon="🏠",  # House emoji for home page
    layout="centered"  # Center everything on the page
)

# Main title of the home page
st.title("CST1510 Multi-Domain Intelligence Platform")

# Subtitle using markdown formatting
st.markdown("## Welcome to the Intelligence Platform")

# Welcome message explaining what the app does
st.write("""
This platform provides integrated access to multiple intelligence domains:

🔐 **Authentication & Security** - Secure login and user management
🛡️ **Cybersecurity** - Monitor and analyze security incidents
📊 **Data Science** - Explore and analyze datasets
💻 **IT Operations** - Manage IT support tickets
🤖 **AI Assistant** - Get insights and answers using AI

### Getting Started:
1. Click on **Login** in the sidebar to access the platform
2. Navigate between domains using the sidebar menu
3. Use the AI Assistant for intelligent insights
""")

# Information box with navigation hint
st.info("Use the sidebar to navigate to different domains!")

# SIDEBAR NAVIGATION - appears on left side
with st.sidebar:
    st.header("Navigation")  # Sidebar title
    
    # Navigation buttons to different pages
    if st.button("Login"):
        st.switch_page("pages/1_Login.py")  # Go to login page
    
    if st.button("Cybersecurity"):
        st.switch_page("pages/2_Cyber_Security.py")  # Go to cybersecurity dashboard
    
    if st.button("Data Science"):
        st.switch_page("pages/3_Data_Science.py")  # Go to data science dashboard
    
    if st.button("IT Operations"):
        st.switch_page("pages/4_IT_Operations.py")  # Go to IT operations dashboard
    
    if st.button("AI Assistant"):
        st.switch_page("pages/5_AI_Assistant.py")  # Go to AI assistant
    
    st.divider()  # Horizontal line in sidebar
    
    # Footer in sidebar
    st.caption("CST1510 Multi-Domain Intelligence Platform ")
    
# End of my code