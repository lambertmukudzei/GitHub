# CST1510 IT Support dashboard
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(
    page_title="IT Support Dashboard",
    page_icon="🎫",
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
def load_tickets_data():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df

# Page header
st.title("IT Support Dashboard")
st.write(f"Managing IT tickets for {st.session_state.username}")

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    st.write(f"**Viewing:** IT Support Tickets")
with col3:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.divider()

# Load data
tickets_df = load_tickets_data()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    
    priority_options = tickets_df['priority'].unique()
    selected_priority = st.multiselect(
        "Priority",
        options=priority_options,
        default=priority_options
    )
    
    status_options = tickets_df['status'].unique()
    selected_status = st.multiselect(
        "Status",
        options=status_options,
        default=status_options
    )
    
    # Resolution time filter if available
    if 'resolution_time_hours' in tickets_df.columns:
        min_time = int(tickets_df['resolution_time_hours'].min()) if not tickets_df.empty else 0
        max_time = int(tickets_df['resolution_time_hours'].max()) if not tickets_df.empty else 100
        resolution_filter = st.slider(
            "Max resolution time (hours)",
            min_value=min_time,
            max_value=max_time,
            value=max_time
        )

# Apply filters
filtered_df = tickets_df[
    (tickets_df['priority'].isin(selected_priority)) &
    (tickets_df['status'].isin(selected_status))
]

# Additional filter for resolution time
if 'resolution_time_hours' in tickets_df.columns and 'resolution_filter' in locals():
    filtered_df = filtered_df[filtered_df['resolution_time_hours'] <= resolution_filter]

# Metrics
st.header("Ticket Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_tickets = len(filtered_df)
    st.metric("Total Tickets", total_tickets)

with col2:
    critical_tickets = len(filtered_df[filtered_df['priority'] == 'Critical'])
    st.metric("Critical", critical_tickets)

with col3:
    open_tickets = len(filtered_df[filtered_df['status'] == 'Open'])
    st.metric("Open", open_tickets)

with col4:
    if 'resolution_time_hours' in filtered_df.columns:
        avg_resolution = filtered_df[filtered_df['status'] == 'Resolved']['resolution_time_hours'].mean()
        st.metric("Avg Resolution", f"{avg_resolution:.1f}h")
    else:
        resolved_count = len(filtered_df[filtered_df['status'] == 'Resolved'])
        st.metric("Resolved", resolved_count)

# Charts
st.header("Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tickets by Priority")
    priority_chart = filtered_df['priority'].value_counts()
    st.bar_chart(priority_chart)
    
    st.subheader("Tickets by Status")
    status_chart = filtered_df['status'].value_counts()
    st.bar_chart(status_chart)

with col2:
    st.subheader("Assignment Distribution")
    if 'assigned_to' in filtered_df.columns:
        assignment_chart = filtered_df['assigned_to'].value_counts()
        st.bar_chart(assignment_chart)
    
    # Resolution time analysis for resolved tickets
    if 'resolution_time_hours' in filtered_df.columns:
        resolved_tickets = filtered_df[filtered_df['status'] == 'Resolved']
        if not resolved_tickets.empty:
            st.subheader("Resolution Time by Priority")
            resolution_by_priority = resolved_tickets.groupby('priority')['resolution_time_hours'].mean()
            st.bar_chart(resolution_by_priority)

# Data table
st.header("Ticket Details")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.divider()
st.caption(f"Showing {len(filtered_df)} of {len(tickets_df)} total tickets")
st.caption("Data from Week 8 database | Real IT ticket data from my project")