#Main dashboard after login
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Dashboard - Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

#Checking Login Status
# This protects the page - users must be logged in to access th page
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 You must be logged in to view this page.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

#Database Connection
def connect_database():
    db_path = Path("DATA") / "intelligence_platform.db"
    return sqlite3.connect(str(db_path))

# Load data from my Week 8 database
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_dashboard_data():
    conn = connect_database()
    
    #Get counts
    incidents_count = pd.read_sql_query("SELECT COUNT(*) FROM cyber_incidents", conn).iloc[0,0]
    tickets_count = pd.read_sql_query("SELECT COUNT(*) FROM it_tickets", conn).iloc[0,0]
    datasets_count = pd.read_sql_query("SELECT COUNT(*) FROM datasets_metadata", conn).iloc[0,0]
    
    #Get sample data for charts
    incidents_df = pd.read_sql_query("SELECT severity, category, status FROM cyber_incidents", conn)
    tickets_df = pd.read_sql_query("SELECT priority, status FROM it_tickets", conn)
    
    conn.close()
    
    return {
        "incidents_count": incidents_count,
        "tickets_count": tickets_count,
        "datasets_count": datasets_count,
        "incidents_df": incidents_df,
        "tickets_df": tickets_df
    }

#Page Header
st.title(f"📊 Welcome, {st.session_state.username}!")
st.write(f"**Role:** {st.session_state.user_role}")

#Quick navigation
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🔐 Cyber Security", use_container_width=True):
        st.switch_page("pages/2_Cyber_Security.py")
with col2:
    if st.button("🎫 IT Support", use_container_width=True):
        st.switch_page("pages/3_IT_Support.py")
with col3:
    if st.button("📊 Data Management", use_container_width=True):
        st.switch_page("pages/4_Data_Management.py")
with col4:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.switch_page("Home.py")

st.divider()

#Load Data
data = load_dashboard_data()

#Key Metrics
st.header("📈 Platform Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Cyber Incidents", data["incidents_count"])
    critical_incidents = len(data["incidents_df"][data["incidents_df"]["severity"] == "Critical"])
    st.caption(f"{critical_incidents} critical")

with col2:
    st.metric("IT Tickets", data["tickets_count"])
    open_tickets = len(data["tickets_df"][data["tickets_df"]["status"] == "Open"])
    st.caption(f"{open_tickets} open")

with col3:
    st.metric("Datasets", data["datasets_count"])
    st.caption("From Week 8 database")

with col4:
    st.metric("Your Role", st.session_state.user_role)
    st.caption("Access level")

#Charts Section
st.header("📊 Quick Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cyber Incidents by Severity")
    severity_counts = data["incidents_df"]["severity"].value_counts()
    st.bar_chart(severity_counts)
    
    st.subheader("Incident Status")
    incident_status = data["incidents_df"]["status"].value_counts()
    st.bar_chart(incident_status)

with col2:
    st.subheader("IT Tickets by Priority")
    priority_counts = data["tickets_df"]["priority"].value_counts()
    st.bar_chart(priority_counts)
    
    st.subheader("Ticket Status")
    ticket_status = data["tickets_df"]["status"].value_counts()
    st.bar_chart(ticket_status)

#Recent Activity
st.header("🔄 Recent Activity")

#Create some demo activity data
activity_data = pd.DataFrame({
    "Time": ["10:30 AM", "11:15 AM", "2:45 PM", "4:20 PM", "5:00 PM"],
    "Action": ["User logged in", "New incident reported", "Ticket resolved", "Dataset uploaded", "Report generated"],
    "User": [st.session_state.username, "Security Team", "IT Support", "Data Team", st.session_state.username]
})

st.dataframe(activity_data, use_container_width=True)

#Quick Actions
st.header("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Report New Incident", use_container_width=True):
        st.info("Incident reporting feature coming soon!")
    
with col2:
    if st.button("🎫 Create IT Ticket", use_container_width=True):
        st.info("Ticket creation feature coming soon!")
    
with col3:
    if st.button("📊 Generate Report", use_container_width=True):
        st.info("Report generation feature coming soon!")

# My Footer
st.divider()
st.caption(f"Logged in as: {st.session_state.username} | Session active")
st.caption("🔒 Secure authentication from Week 7 | 🗄️ Real data from my Week 8 database")