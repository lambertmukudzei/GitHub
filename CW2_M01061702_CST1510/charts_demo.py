# This is my charts demo file, learning how to make different types of charts
import streamlit as st  # For building web app
import pandas as pd  # For working with data tables
import numpy as np  # For math and generating random numbers

# We must start with the page configuration
st.set_page_config(
    page_title="Charts Demo",  # Browser tab title
    page_icon="📊",  # Chart emoji in tab
    layout="wide"  # Use full screen width
)

# Main page title and description
st.title("📊 Charts Demo")
st.write("Learning to create charts with Streamlit")

# Function to create fake data for testing
def create_demo_data():
    """Create sample data for charts when real data isn't available"""
    # Fake cybersecurity incidents data
    incidents_data = {
        'severity': ['Critical'] * 5 + ['High'] * 15 + ['Medium'] * 60 + ['Low'] * 35,
        'category': ['Phishing'] * 40 + ['Malware'] * 30 + ['DDoS'] * 20 + ['Unauthorized Access'] * 25,
        'status': ['Open'] * 30 + ['Resolved'] * 60 + ['In Progress'] * 25
    }
    
    # Fake IT tickets data  
    tickets_data = {
        'priority': ['Critical'] * 10 + ['High'] * 40 + ['Medium'] * 70 + ['Low'] * 30,
        'status': ['Open'] * 25 + ['Resolved'] * 80 + ['In Progress'] * 30 + ['Waiting for User'] * 15,
        'resolution_time_hours': list(np.random.randint(1, 50, 100)) + list(np.random.randint(50, 100, 50))
    }
    
    return pd.DataFrame(incidents_data), pd.DataFrame(tickets_data)

# Try to load real data from database, use fake data if it fails
def try_load_real_data():
    """Try to load real data, but use demo data if it fails"""
    try:
        import sqlite3
        from pathlib import Path
        
        # Check if database file exists
        db_path = Path("DATA/intelligence_platform.db")
        if db_path.exists():
            # Connect to database
            conn = sqlite3.connect(str(db_path))
            
            # Try to get real data from database tables
            incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
            tickets_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
            
            conn.close()  # Close database connection
            
            # Check if we got actual data
            if not incidents_df.empty and not tickets_df.empty:
                st.success("Successfully Loaded my real Week 8 data!")
                return incidents_df, tickets_df, True  # True means real data
    except Exception as e:
        st.write(f"Note: {e}")  # Show error if something goes wrong
    
    # If we get here, something failed - use demo data
    incidents_df, tickets_df = create_demo_data()
    st.info("Using demo data. Run `python main.py` to see your real data!")
    return incidents_df, tickets_df, False  # False means demo data

# Load the data (real or fake)
incidents_df, tickets_df, is_real_data = try_load_real_data()

# Show data overview at top
st.header("Data Overview")
col1, col2 = st.columns(2)  # Two columns for metrics

with col1:
    st.metric("Cyber Incidents", len(incidents_df))  # Count of incidents
    st.metric("Unique Severities", incidents_df['severity'].nunique())  # Count of unique severity levels

with col2:
    st.metric("IT Tickets", len(tickets_df))  # Count of tickets
    st.metric("Ticket Priorities", tickets_df['priority'].nunique())  # Count of unique priority levels

st.divider()  # Horizontal line

# Create charts section
st.header("📊 Creating Charts with Streamlit")

# BAR CHARTS SECTION
st.subheader("📊 Bar Charts")
st.write("Bar charts are great for comparing categories")

col1, col2 = st.columns(2)  # Two columns for side-by-side charts

with col1:
    st.write("**Cyber Incidents by Severity**")
    severity_counts = incidents_df['severity'].value_counts()  # Count how many of each severity
    st.bar_chart(severity_counts)  # Make bar chart

with col2:
    st.write("**IT Tickets by Priority**")
    priority_counts = tickets_df['priority'].value_counts()  # Count how many of each priority
    st.bar_chart(priority_counts)  # Make bar chart

# MORE BAR CHARTS
st.subheader("More Bar Charts")

col1, col2 = st.columns(2)  # Two more columns

with col1:
    st.write("**Incidents by Category**")
    category_counts = incidents_df['category'].value_counts()  # Count incidents by category
    st.bar_chart(category_counts)

with col2:
    st.write("**Tickets by Status**")
    status_counts = tickets_df['status'].value_counts()  # Count tickets by status
    st.bar_chart(status_counts)

st.divider()  # Horizontal line

# LINE AND AREA CHARTS SECTION
st.header("📈 Line and Area Charts")
st.write("Line and area charts show trends over time")

# Create fake time series data (dates and values)
dates = pd.date_range('2024-01-01', periods=50, freq='D')  # 50 days starting Jan 1, 2024
line_data = pd.DataFrame({
    'date': dates,
    'value1': np.random.randn(50).cumsum() + 100,  # Random walk starting at 100
    'value2': np.random.randn(50).cumsum() + 150,  # Random walk starting at 150
    'value3': np.random.randn(50).cumsum() + 200   # Random walk starting at 200
})

col1, col2 = st.columns(2)  # Two columns for charts

with col1:
    st.write("**Line Chart - Multiple Series**")
    st.line_chart(line_data.set_index('date'))  # Line chart with date on x-axis

with col2:
    st.write("**Area Chart - Single Series**")
    st.area_chart(line_data.set_index('date')['value1'])  # Area chart with just value1

st.divider()  # Horizontal line

# ADVANCED CHARTS SECTION
st.header("Advanced Chart Examples")

# If we have real data with resolution times, show real analysis
if is_real_data and 'resolution_time_hours' in tickets_df.columns:
    st.subheader("Real Data Analysis")
    
    # Filter to only resolved tickets
    resolved_tickets = tickets_df[tickets_df['status'] == 'Resolved']
    
    if not resolved_tickets.empty:  # If we have resolved tickets
        # Group by priority and calculate average resolution time
        resolution_by_priority = resolved_tickets.groupby('priority')['resolution_time_hours'].mean()
        
        col1, col2 = st.columns(2)  # Two columns for charts
        
        with col1:
            st.write("**Average Resolution Time by Priority**")
            st.bar_chart(resolution_by_priority)  # Bar chart of average times
        
        with col2:
            st.write("**Resolution Time Distribution**")
            # Area chart of resolution times (first 30 tickets)
            st.area_chart(resolved_tickets['resolution_time_hours'].head(30))
    else:
        st.info("No resolved tickets in the data")  # Message if no resolved tickets
else:
    # Show demo analysis if we don't have real data
    st.subheader("Demo Data Analysis")
    
    col1, col2 = st.columns(2)  # Two columns for demo charts
    
    with col1:
        st.write("**Demo: Incident Status by Severity**")
        # Create cross-tabulation (severity vs status)
        demo_cross = pd.crosstab(incidents_df['severity'], incidents_df['status'])
        st.bar_chart(demo_cross)  # Bar chart of the cross-tab
    
    with col2:
        st.write("**Demo: Random Trend Data**")
        # Create random trend data
        trend_data = pd.DataFrame({
            'trend': np.random.randn(30).cumsum() + 50  # Random walk starting at 50
        })
        st.line_chart(trend_data)  # Line chart of trend

st.divider()  # Horizontal line

# DATA TABLES SECTION (show raw data)
st.header("View the Raw Data")

# Create tabs for different data types
tab1, tab2 = st.tabs(["Cyber Incidents", "IT Tickets"])

with tab1:
    st.subheader("Cyber Incidents Data")
    st.dataframe(incidents_df.head(10))  # Show first 10 rows

with tab2:
    st.subheader("IT Tickets Data")
    st.dataframe(tickets_df.head(10))  # Show first 10 rows

# Success message at bottom
st.success("I've learned how to create charts with Streamlit!")