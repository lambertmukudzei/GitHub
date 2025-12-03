import streamlit as st
import pandas as pd
import numpy as np

#We start off with Page configuration
st.set_page_config(
    page_title="My Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 My Intelligence Platform Dashboard")
st.write("A complete dashboard showing data visualization")

# we must Create reliable demo data
def create_demo_data():
    np.random.seed(42)  # For consistent results
    
    # Users data
    users_data = {
        'username': ['Kevin12345', 'Mukudzei', 'Middlesex', 'test_user', 'admin_user'],
        'role': ['user', 'user', 'user', 'analyst', 'admin']
    }
    
    # Cyber incidents data
    incidents_data = {
        'incident_id': range(1000, 1115),
        'severity': ['Critical'] * 10 + ['High'] * 25 + ['Medium'] * 50 + ['Low'] * 30,
        'category': ['Phishing'] * 45 + ['Malware'] * 35 + ['DDoS'] * 15 + ['Unauthorized Access'] * 20,
        'status': ['Open'] * 25 + ['Resolved'] * 70 + ['In Progress'] * 15 + ['Closed'] * 5,
        'description': [f'Incident {i} description' for i in range(115)]
    }
    
    # IT tickets data
    tickets_data = {
        'ticket_id': range(2000, 2150),
        'priority': ['Critical'] * 15 + ['High'] * 45 + ['Medium'] * 60 + ['Low'] * 30,
        'status': ['Open'] * 30 + ['Resolved'] * 80 + ['In Progress'] * 25 + ['Waiting for User'] * 15,
        'assigned_to': ['IT_Support_A'] * 50 + ['IT_Support_B'] * 50 + ['IT_Support_C'] * 50,
        'resolution_time_hours': list(np.random.randint(1, 24, 100)) + list(np.random.randint(24, 168, 50))
    }
    
    # Datasets data
    datasets_data = {
        'name': ['Customer_Churn', 'Financial_Fraud', 'Server_Logs', 'Image_Classification', 'HR_Salary'],
        'rows': [5000, 150000, 800000, 1000, 3000],
        'columns': [15, 22, 10, 5, 12],
        'uploaded_by': ['data_scientist', 'cyber_admin', 'data_scientist', 'data_scientist', 'it_admin']
    }
    
    return {
        'users': pd.DataFrame(users_data),
        'incidents': pd.DataFrame(incidents_data),
        'tickets': pd.DataFrame(tickets_data),
        'datasets': pd.DataFrame(datasets_data)
    }

# Try to load real data
def try_load_real_data():
    """Try to load real data, fall back to demo data"""
    try:
        import sqlite3
        from pathlib import Path
        
        db_path = Path("DATA/intelligence_platform.db")
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            
            users_df = pd.read_sql_query("SELECT username, role FROM users", conn)
            incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
            tickets_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
            datasets_df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
            
            conn.close()
            
            if not users_df.empty:
                st.success("✅ Loaded your REAL Week 8 data!")
                return {
                    'users': users_df,
                    'incidents': incidents_df,
                    'tickets': tickets_df,
                    'datasets': datasets_df
                }, True
    except Exception as e:
        st.write(f"Note: {e}")
    
    # Fall back to demo data
    demo_data = create_demo_data()
    st.info("📝 Using demo data. Run `python main.py` to see your real data!")
    return demo_data, False

# Load data
data, is_real_data = try_load_real_data()

# ---- SIDEBAR ----
with st.sidebar:
    st.header("🎛️ Dashboard Controls")
    
    # View selector
    selected_view = st.radio(
        "Choose Dashboard View:",
        ["Overview", "Security Center", "IT Support", "Data Management", "User Analytics"]
    )
    
    # Data filters
    st.subheader("🔍 Data Filters")
    
    # Incident filters
    severity_options = data['incidents']['severity'].unique()
    selected_severities = st.multiselect(
        "Incident Severity:",
        options=severity_options,
        default=severity_options
    )
    
    # Ticket filters
    priority_options = data['tickets']['priority'].unique()
    selected_priorities = st.multiselect(
        "Ticket Priority:",
        options=priority_options,
        default=priority_options
    )
    
    st.divider()
    st.write("**Project Info**")
    st.write("Week 7: Authentication System")
    st.write("Week 8: Database & CRUD")
    st.write("Streamlit: Web Dashboard")

# Apply filters
filtered_incidents = data['incidents'][data['incidents']['severity'].isin(selected_severities)]
filtered_tickets = data['tickets'][data['tickets']['priority'].isin(selected_priorities)]

# ---- MAIN DASHBOARD CONTENT ----
if selected_view == "Overview":
    st.header("🏠 Platform Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_incidents = len(filtered_incidents)
        critical_incidents = len(filtered_incidents[filtered_incidents['severity'] == 'Critical'])
        st.metric("Cyber Incidents", total_incidents, f"{critical_incidents} critical")
    
    with col2:
        total_tickets = len(filtered_tickets)
        open_tickets = len(filtered_tickets[filtered_tickets['status'] == 'Open'])
        st.metric("IT Tickets", total_tickets, f"{open_tickets} open")
    
    with col3:
        total_datasets = len(data['datasets'])
        total_rows = data['datasets']['rows'].sum()
        st.metric("Datasets", total_datasets, f"{total_rows:,} rows")
    
    with col4:
        total_users = len(data['users'])
        analysts = len(data['users'][data['users']['role'] == 'analyst'])
        st.metric("Users", total_users, f"{analysts} analysts")
    
    # Quick charts
    st.subheader("📊 Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Incident Severity Distribution**")
        severity_chart = filtered_incidents['severity'].value_counts()
        st.bar_chart(severity_chart)
    
    with col2:
        st.write("**Ticket Priority Distribution**")
        priority_chart = filtered_tickets['priority'].value_counts()
        st.bar_chart(priority_chart)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Incident Status**")
        status_chart = filtered_incidents['status'].value_counts()
        st.bar_chart(status_chart)
    
    with col2:
        st.write("**Ticket Status**")
        ticket_status_chart = filtered_tickets['status'].value_counts()
        st.bar_chart(ticket_status_chart)

elif selected_view == "Security Center":
    st.header("🔐 Security Center")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incident Analysis")
        
        st.write("**By Severity Level**")
        st.bar_chart(filtered_incidents['severity'].value_counts())
        
        st.write("**By Category**")
        st.bar_chart(filtered_incidents['category'].value_counts())
    
    with col2:
        st.subheader("Status Overview")
        
        st.write("**Current Status**")
        st.bar_chart(filtered_incidents['status'].value_counts())
        
        # Quick statistivs
        open_count = len(filtered_incidents[filtered_incidents['status'] == 'Open'])
        resolved_count = len(filtered_incidents[filtered_incidents['status'] == 'Resolved'])
        
        st.metric("Open Incidents", open_count)
        st.metric("Resolved Incidents", resolved_count)
    
    # Incident details
    with st.expander("📋 View Incident Details"):
        st.dataframe(filtered_incidents)

elif selected_view == "IT Support":
    st.header("🎫 IT Support Center")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ticket Analysis")
        
        st.write("**By Priority**")
        st.bar_chart(filtered_tickets['priority'].value_counts())
        
        st.write("**By Status**")
        st.bar_chart(filtered_tickets['status'].value_counts())
    
    with col2:
        st.subheader("Support Team")
        
        st.write("**Assignment Distribution**")
        st.bar_chart(filtered_tickets['assigned_to'].value_counts())
        
        # Support metrics
        if 'resolution_time_hours' in filtered_tickets.columns:
            resolved_tickets = filtered_tickets[filtered_tickets['status'] == 'Resolved']
            if not resolved_tickets.empty:
                avg_resolution = resolved_tickets['resolution_time_hours'].mean()
                st.metric("Avg Resolution Time", f"{avg_resolution:.1f} hours")
    
    # Ticket details
    with st.expander("📋 View Ticket Details"):
        st.dataframe(filtered_tickets)

elif selected_view == "Data Management":
    st.header("📊 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Overview")
        
        st.write("**Dataset Sizes**")
        dataset_sizes = data['datasets'].set_index('name')['rows']
        st.bar_chart(dataset_sizes)
        
        total_storage = data['datasets']['rows'].sum()
        st.metric("Total Rows", f"{total_storage:,}")
    
    with col2:
        st.subheader("Dataset Details")
        st.dataframe(data['datasets'])
        
        avg_rows = data['datasets']['rows'].mean()
        st.metric("Average Rows per Dataset", f"{avg_rows:,.0f}")

else:  # User Analytics
    st.header("👥 User Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Roles")
        role_counts = data['users']['role'].value_counts()
        st.bar_chart(role_counts)
        
        st.metric("Total Users", len(data['users']))
    
    with col2:
        st.subheader("User Information")
        st.dataframe(data['users'])
        
        unique_roles = data['users']['role'].nunique()
        st.metric("Unique Roles", unique_roles)

#FOOTER
st.divider()
st.success("🚀 Dashboard loaded successfully!")
st.info("""
**This dashboard demonstrates:**
- **Interactive filtering** with sidebar controls
- **Multiple view types** for different data perspectives  
- **Real-time charts** that update with filters
- **Professional layout** with columns and metrics
- **My Week 8 data** (or demo data for learning)
""")