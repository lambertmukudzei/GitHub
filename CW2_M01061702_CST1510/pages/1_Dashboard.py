# 1_Dashboard.py -My Main dashboard page for the intelligence platform
import streamlit as st  # For building web interface
import pandas as pd  # For working with data tables
import sqlite3  # For database operations
from pathlib import Path  # For handling file paths

# We start off with Page configuration
st.set_page_config(
    page_title="Dashboard CST1510 Intelligence Platform",  # Browser tab title
    page_icon="📊",  # Chart emoji in tab
    layout="wide"  # Use full screen width
)

# SECURITY CHECK - Must be logged in to see this page
if not st.session_state.get("logged_in"):  # Check if user is logged in
    st.error("You must be logged in to view this page.")  # Error message
    st.stop()  # Stop running code - can't see page

# Database Connection function
def connect_database():
    # Path to database file in DATA folder
    db_path = Path("DATA") / "intelligence_platform.db"
    return sqlite3.connect(str(db_path))  # Connect to SQLite database

# Load data from database with caching (makes it faster)
@st.cache_data(ttl=300)  # Cache for 5 minutes (300 seconds)
def load_dashboard_data():
    conn = connect_database()  # Open database connection
    
    # Get counts from different tables
    incidents_count = pd.read_sql_query("SELECT COUNT(*) FROM cyber_incidents", conn).iloc[0,0]
    tickets_count = pd.read_sql_query("SELECT COUNT(*) FROM it_tickets", conn).iloc[0,0]
    datasets_count = pd.read_sql_query("SELECT COUNT(*) FROM datasets_metadata", conn).iloc[0,0]
    
    # Get data for charts
    incidents_df = pd.read_sql_query("SELECT severity, category, status FROM cyber_incidents", conn)
    tickets_df = pd.read_sql_query("SELECT priority, status FROM it_tickets", conn)
    
    conn.close()  # Close database connection
    
    # Return all data in a dictionary
    return {
        "incidents_count": incidents_count,
        "tickets_count": tickets_count,
        "datasets_count": datasets_count,
        "incidents_df": incidents_df,
        "tickets_df": tickets_df
    }

# PAGE HEADER - Welcome message
st.title(f"Welcome, {st.session_state.username}!")  # Personalized title
st.write(f"**Role:** {st.session_state.user_role}")  # Show user's role

# NAVIGATION BAR - Buttons to switch between pages
st.header("Navigation")

# Create 5 equal columns for navigation buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    # Cyber Security button - would normally switch to cyber page
    if st.button("Cyber Security", use_container_width=True):
        st.session_state.page = "cyber"  # Set which page to show
        st.rerun()  # Refresh page (would normally switch)

with col2:
    # IT Support button
    if st.button("IT Support", use_container_width=True):
        st.session_state.page = "it"
        st.rerun()

with col3:
    # Data Management button
    if st.button("Data Management", use_container_width=True):
        st.session_state.page = "data"
        st.rerun()

with col4:
    # AI Assistant button
    if st.button("AI Assistant", use_container_width=True):
        st.session_state.page = "ai"
        st.rerun()

with col5:
    # Logout button (secondary color = less prominent)
    if st.button("Logout", use_container_width=True, type="secondary"):
        # Clear all user data from session
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.page = "login"
        st.rerun()  # Refresh to go to login

st.divider()  # Horizontal line

# LOAD DATA FROM DATABASE
data = load_dashboard_data()

# The key metrics section - Numbers at top
st.header("Platform Overview")

# Create 4 columns for metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Cyber Incidents", data["incidents_count"])  # Total incidents
    # Count critical incidents
    critical = len(data["incidents_df"][data["incidents_df"]["severity"] == "Critical"])
    st.caption(f"{critical} critical")  # Small text below metric

with col2:
    st.metric("IT Tickets", data["tickets_count"])  # Total tickets
    # Count open tickets
    open_tickets = len(data["tickets_df"][data["tickets_df"]["status"] == "Open"])
    st.caption(f"{open_tickets} open")

with col3:
    st.metric("Datasets", data["datasets_count"])  # Total datasets
    st.caption("From database")  # Source of data

with col4:
    st.metric("Your Role", st.session_state.user_role)  # User's role
    st.caption("Access level")  # What role means

# CHARTS SECTION - Visual data
st.header("Quick Insights")

# Two columns for side-by-side charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cyber Incidents by Severity")
    # Count incidents by severity level
    severity_counts = data["incidents_df"]["severity"].value_counts()
    st.bar_chart(severity_counts)  # Bar chart of counts
    
    st.subheader("Incident Status")
    # Count incidents by status (Open, Resolved, etc.)
    incident_status = data["incidents_df"]["status"].value_counts()
    st.bar_chart(incident_status)

with col2:
    st.subheader("IT Tickets by Priority")
    # Count tickets by priority (High, Medium, Low)
    priority_counts = data["tickets_df"]["priority"].value_counts()
    st.bar_chart(priority_counts)
    
    st.subheader("Ticket Status")
    # Count tickets by status
    ticket_status = data["tickets_df"]["status"].value_counts()
    st.bar_chart(ticket_status)

# RECENT ACTIVITY SECTION
st.header("Recent Activity")

# Create fake activity data (hardcoded for demo)
activity_data = pd.DataFrame({
    "Time": ["10:30 AM", "11:15 AM", "2:45 PM"],
    "Action": ["User logged in", "New incident reported", "Ticket resolved"],
    "User": [st.session_state.username, "Security Team", "IT Support"]
})
st.dataframe(activity_data, use_container_width=True)  # Show as table

# QUICK ACTIONS SECTION
st.header("Quick Actions")

# Three columns for action buttons
col1, col2, col3 = st.columns(3)

with col1:
    # Button to report new incident
    if st.button("Report New Incident", use_container_width=True):
        st.info("Incident reporting feature")  # Would normally open form

with col2:
    # Button to create IT ticket
    if st.button("Create IT Ticket", use_container_width=True):
        st.info("Ticket creation feature")  # Would normally open form

with col3:
    # Button to generate report
    if st.button("Generate Report", use_container_width=True):
        st.info("Report generation feature")  # Would normally create report

# FOOTER at bottom
st.divider()  # Horizontal line
st.caption(f"Logged in as: {st.session_state.username}")  # Shows who's logged in
st.caption("Multi-Domain Intelligence Platform")  # App name