#Cyber incidents dashboard
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(
    page_title="Cyber Security Dashboard",
    page_icon="🔐",
    layout="wide"
)

# Check login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in!")
    st.switch_page("Home.py")
    st.stop()

# Database connection
def connect_database():
    db_path = Path("DATA") / "intelligence_platform.db"
    return sqlite3.connect(str(db_path))

@st.cache_data(ttl=300)
def load_incidents_data():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

# Page header
st.title("🔐 Cyber Security Dashboard")
st.write(f"Welcome, {st.session_state.username}! Analyzing security incidents.")

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    st.write(f"**Viewing:** Cyber Incidents")
with col3:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.divider()

# Load data
incidents_df = load_incidents_data()

#Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    severity_options = incidents_df['severity'].unique()
    selected_severity = st.multiselect(
        "Severity",
        options=severity_options,
        default=severity_options
    )
    
    category_options = incidents_df['category'].unique()
    selected_category = st.multiselect(
        "Category",
        options=category_options,
        default=category_options
    )
    
    status_options = incidents_df['status'].unique()
    selected_status = st.multiselect(
        "Status",
        options=status_options,
        default=status_options
    )

# Apply filters
filtered_df = incidents_df[
    (incidents_df['severity'].isin(selected_severity)) &
    (incidents_df['category'].isin(selected_category)) &
    (incidents_df['status'].isin(selected_status))
]

# Metrics
st.header("📊 Incident Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_incidents = len(filtered_df)
    st.metric("Total Incidents", total_incidents)

with col2:
    critical_count = len(filtered_df[filtered_df['severity'] == 'Critical'])
    st.metric("Critical", critical_count)

with col3:
    open_count = len(filtered_df[filtered_df['status'] == 'Open'])
    st.metric("Open", open_count)

with col4:
    phishing_count = len(filtered_df[filtered_df['category'] == 'Phishing'])
    st.metric("Phishing", phishing_count)

# Charts
st.header("📈 Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Severity")
    severity_chart = filtered_df['severity'].value_counts()
    st.bar_chart(severity_chart)
    
    st.subheader("Incidents by Category")
    category_chart = filtered_df['category'].value_counts()
    st.bar_chart(category_chart)

with col2:
    st.subheader("Incidents by Status")
    status_chart = filtered_df['status'].value_counts()
    st.bar_chart(status_chart)
    
    #Create a time-based chart if timestamp exists
    if 'timestamp' in filtered_df.columns and not filtered_df['timestamp'].empty:
        st.subheader("Incidents Over Time")
        # Simple line chart showing count by some metric
        st.line_chart(filtered_df['severity'].value_counts())

# Data table
st.header("📋 Incident Details")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.divider()
st.caption(f"Showing {len(filtered_df)} of {len(incidents_df)} total incidents")
st.caption("Data from Week 8 database | Real incident data from my project")