#My 2_Cyber_Security.py
#Student ID: M01061702
#This is the main dashboard page after logging in
import streamlit as st #-For the Webpage
import pandas as pd # For working with tables of data
from services.database_manager import DatabaseManager # My database handler
from models.security_incidents import SecurityIncident # where we get our security incidents

#We start off by setting up the page
st.set_page_config(
    page_title="CST1510 Cybersecurity Dashboard",
    page_icon="🛡️", # The little shield icon to make my dashboard look proffesional 
    layout="wide"
)

# CHECK AUTHENTICATION
# Checking if the user is logged in for security purposes
#This is Important because We don't want people seeing this page without logging in first
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Hi, Please login to access this page!")
    if st.button("Go to Login"):
        st.switch_page("pages/1_Login.py")
    st.stop()
# HEADER
col1, col2 = st.columns([3, 1]) # Creates two columns, the big one (3 parts) and small one (1 part)
with col1:
    st.title("CST1510 Cybersecurity Dashboard")
    st.write(f"Welcome, **{st.session_state.username}**!")
with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.current_user = None
        st.switch_page("pages/1_Login.py")

# DATABASE CONNECTION
@st.cache_resource # Caches this so we don't connect every time page refreshes
def get_db_manager():
    return DatabaseManager()

db_manager = get_db_manager() # Actually creates the database connection

#The  MAIN CONTENT
st.subheader("Security Incidents Overview")

#Fetch data
incidents_data = db_manager.fetch_all("SELECT * FROM cyber_incidents")
# FETCHING DATA FROM DATABASE
# Getting all security incidents from the cyber_incidents table

if incidents_data:
     # Converting the date into a Pandas DataFrame
    # DataFrames are like Excel spreadsheets in code - easy to work with
    df = pd.DataFrame(incidents_data, columns=[
        'incident_id', 'timestamp', 'severity', 'category', 
        'status', 'description', 'created_at'
    ])
    
    #Creating Metrics (THE NUMBER BOXES AT THE TOP)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", len(df))
    with col2:
        critical = len(df[df['severity'] == 'Critical'])
        st.metric("Critical", critical, delta_color="inverse")
    with col3:
        open_incidents = len(df[df['status'] == 'Open'])
        st.metric("Open", open_incidents)
    with col4:
        resolved = len(df[df['status'] == 'Resolved'])
        st.metric("Resolved", resolved)
    
    st.divider()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=df['severity'].unique(),
            default=df['severity'].unique()
        )
    with col2:
         # Multi-select dropdown for status (Open, Investigating, Resolved)
        status_filter = st.multiselect(
            "Filter by Status",
            options=df['status'].unique(),
            default=df['status'].unique()
        )
    with col3:
        category_filter = st.multiselect(
            "Filter by Category",
            options=df['category'].unique(),
            default=df['category'].unique()
        )
    
    # Apply filters
    filtered_df = df[
        (df['severity'].isin(severity_filter)) & # Include rows with selected severity
        (df['status'].isin(status_filter)) & # and selected status
        (df['category'].isin(category_filter)) # and selected category
    ]
    
    # Display table
    st.subheader(f"Security Incidents ({len(filtered_df)} found)")
    st.dataframe(
        filtered_df[['incident_id', 'timestamp', 'severity', 'category', 'status', 'description']],
        use_container_width=True
    )
    
    # Incident Details
    st.subheader("Incident Details")
    # Let user select specific incidents to see more details
    selected_ids = st.multiselect(
        "Select incidents to view details:",
        options=filtered_df['incident_id'].tolist()
    )
    
    if selected_ids:
        for incident_id in selected_ids:
            incident_row = df[df['incident_id'] == incident_id].iloc[0]
            # Creating an expandable section (click to open)
            with st.expander(f"Incident #{incident_id} - {incident_row['category']} ({incident_row['severity']})"):
               # Display all details about this incident
                st.write(f"**Timestamp:** {incident_row['timestamp']}")
                st.write(f"**Severity:** {incident_row['severity']}")
                st.write(f"**Category:** {incident_row['category']}")
                st.write(f"**Status:** {incident_row['status']}")
                st.write(f"**Description:** {incident_row['description']}")
                st.write(f"**Created at:** {incident_row['created_at']}")
    
    # Statistics
    st.subheader("Statistics")
    col1, col2 = st.columns(2)
    with col1:
        # Bar chart showing count of incidents by severity
        st.bar_chart(df['severity'].value_counts())
    with col2:
        st.bar_chart(df['category'].value_counts())
    
else:
    st.info("No security incidents found in the database.")
# SIDEBAR NAVIGATION
with st.sidebar: # Everything in sidebar appears on the left
    st.header(" Navigation")
    st.write("Navigate to other domains:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Data Science"):
            st.switch_page("pages/3_Data_Science.py")
    with col2:
        if st.button("IT Operations"):
            st.switch_page("pages/4_IT_Operations.py")
    
    if st.button("AI Assistant"):
        st.switch_page("pages/5_AI_Assistant.py")
    
    st.divider()  # Horizontal line to seperate sections
    st.caption("CST1510 Cybersecurity Dashboard-M01061702")  #Footer with my student ID
    #End of my Code