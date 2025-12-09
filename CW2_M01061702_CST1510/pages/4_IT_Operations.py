# MY 4_IT_Operations.py
#Student ID: M01061702
# This is my IT Operations Dashboard page, it shows IT support tickets

# Importing libraries I need
import streamlit as st  # For building the web page
import pandas as pd  # For working with data tables
from services.database_manager import DatabaseManager  # My database connection
#Setting up my page 
st.set_page_config(
    page_title="CST1510 IT Operations Dashboard",  # What shows in browser tab
    page_icon="💻",  # Computer emoji in tab
    layout="wide"  # Makes page use full screen width
)

# We must now do an authentication check for security purposes
# Making sure only logged-in users can see this page
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to access this page!")  # Warning message
    if st.button("Go to Login"):  # Button to go back to login
        st.switch_page("pages/1_Login.py")  # Takes user to login page
    st.stop()  # Stops running code here 

# The header at the top of the page
col1, col2 = st.columns([3, 1])  # Creates two columns: big left (3/4) and small right (1/4)
with col1:  # Left column
    st.title("IT Operations Dashboard")  # Main title 
    st.write(f"Welcome, **{st.session_state.username}**!")  # Shows user's name
with col2:  # Right column
    if st.button("Logout"):  # Logout button
        # Clear all user data from memory when logging out
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.current_user = None
        st.switch_page("pages/1_Login.py")  # Go back to login page

# Database connection setup
@st.cache_resource  # Only connects once even if page refreshes
def get_db_manager():
    return DatabaseManager()  # Creates database connection

db_manager = get_db_manager()  # Actually makes the connection

# The main content of my page
st.subheader("IT Tickets Overview")  # Section title

# fetching data from database
# Getting IT tickets from it_tickets table, limiting to 50 so it doesn't get too slow
tickets_data = db_manager.fetch_all("SELECT * FROM it_tickets LIMIT 50")

# Check if we got any data
if tickets_data:
    # convert to pandas dataframe (like an excel TABLE)
    df = pd.DataFrame(tickets_data, columns=[
        'ticket_id', 'priority', 'description', 'status', 
        'assigned_to', 'created_at', 'resolution_time_hours', 'created_at_timestamp'
    ])
    
    # metrics at the top showing key numbers
    col1, col2, col3, col4 = st.columns(4)  # 4 equal columns
    with col1:
        open_tickets = len(df[df['status'] == 'Open'])  # Count open tickets
        st.metric("Open Tickets", open_tickets, delta_color="inverse")  # Red for bad
    with col2:
        high_priority = len(df[df['priority'] == 'High'])  # Count high priority tickets
        st.metric("High Priority", high_priority, delta_color="inverse")  # Also red for bad
    with col3:
        avg_resolution = df['resolution_time_hours'].mean()  # Average time to fix
        st.metric("Avg Resolution (hrs)", f"{avg_resolution:.1f}")  # 1 decimal place
    with col4:
        total_tickets = len(df)  # Total tickets
        st.metric("Total Tickets", total_tickets)
    
    st.divider()  # Horizontal line
    
    # letting thw user filter tickets
    col1, col2, col3 = st.columns(3)  # 3 columns for filters
    with col1:
        # Multi-select for priority (High, Medium, Low)
        priority_filter = st.multiselect(
            "Filter by Priority",
            options=df['priority'].unique(),  # Get all unique priorities
            default=df['priority'].unique()  # Show all by default
        )
    with col2:
        # Multi-select for status (Open, In Progress, Resolved)
        status_filter = st.multiselect(
            "Filter by Status",
            options=df['status'].unique(),
            default=df['status'].unique()
        )
    with col3:
        # Multi-select for who it's assigned to
        assignee_filter = st.multiselect(
            "Filter by Assignee",
            options=df['assigned_to'].unique(),
            default=df['assigned_to'].unique()
        )
    
    # APPLY THE FILTERS USER SELECTED
    filtered_df = df[
        (df['priority'].isin(priority_filter)) &  # Include selected priorities
        (df['status'].isin(status_filter)) &       # AND selected statuses
        (df['assigned_to'].isin(assignee_filter))  # AND selected assignees
    ]
    
    # DISPLAY THE FILTERED TABLE
    st.subheader(f"IT Tickets ({len(filtered_df)} found)")  # Shows how many tickets
    st.dataframe(
        filtered_df[['ticket_id', 'priority', 'description', 'status', 'assigned_to', 'created_at']],
        use_container_width=True  # Makes table use full width
    )
    
    # TICKET DETAILS SECTION
    st.subheader("Ticket Details")
    # Let user select specific tickets to see more info
    selected_ids = st.multiselect(
        "Select tickets to view details:",
        options=filtered_df['ticket_id'].tolist()  # List of all ticket IDs
    )
    
    # If user selected any tickets
    if selected_ids:
        for ticket_id in selected_ids:
            # Get the row for this ticket ID
            ticket_row = df[df['ticket_id'] == ticket_id].iloc[0]
            # Create expandable section (click to open)
            with st.expander(f"Ticket #{ticket_id} - {ticket_row['priority']} Priority"):
                # Show all details about this ticket
                st.write(f"**Priority:** {ticket_row['priority']}")
                st.write(f"**Description:** {ticket_row['description']}")
                st.write(f"**Status:** {ticket_row['status']}")
                st.write(f"**Assigned to:** {ticket_row['assigned_to']}")
                st.write(f"**Created at:** {ticket_row['created_at']}")
                st.write(f"**Resolution time (hours):** {ticket_row['resolution_time_hours']}")
                st.write(f"**Created at (timestamp):** {ticket_row['created_at_timestamp']}")
    
    # STATS CHARTS
    st.subheader("CST1510 Ticket Statistics")
    col1, col2 = st.columns(2)  # Two columns for charts
    with col1:
        # Bar chart showing count of tickets by priority
        st.bar_chart(df['priority'].value_counts())
    with col2:
        # Bar chart showing count of tickets by who they're assigned to
        st.bar_chart(df['assigned_to'].value_counts())
    
else:  # If no data in database
    st.info("No IT tickets found in the database.")

# SIDEBAR NAVIGATION
with st.sidebar:  # Everything here goes in sidebar on left
    st.header("Navigation")
    st.write("Navigate to other domains:")
    
    # Navigation buttons in two columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cybersecurity"):
            st.switch_page("pages/2_Cyber_Security.py")
    with col2:
        if st.button("Data Science"):
            st.switch_page("pages/3_Data_Science.py")
    
    # AI Assistant button
    if st.button("AI Assistant"):
        st.switch_page("pages/5_AI_Assistant.py")
    
    st.divider()  # Horizontal line
    st.caption("CST1510 IT Operations Dashboard-M01061702")  # Footer with my ID
# End of my code