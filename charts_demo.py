import streamlit as st
import pandas as pd
import numpy as np

#We must start with the page configuration
st.set_page_config(
    page_title="Charts Demo",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Charts Demo")
st.write("Learning to create charts with Streamlit")

# Create reliable demo data that always works
def create_demo_data():
    """Create sample data for charts"""
    # Cyber incidents demo data
    incidents_data = {
        'severity': ['Critical'] * 5 + ['High'] * 15 + ['Medium'] * 60 + ['Low'] * 35,
        'category': ['Phishing'] * 40 + ['Malware'] * 30 + ['DDoS'] * 20 + ['Unauthorized Access'] * 25,
        'status': ['Open'] * 30 + ['Resolved'] * 60 + ['In Progress'] * 25
    }
    
    # IT tickets demo data  
    tickets_data = {
        'priority': ['Critical'] * 10 + ['High'] * 40 + ['Medium'] * 70 + ['Low'] * 30,
        'status': ['Open'] * 25 + ['Resolved'] * 80 + ['In Progress'] * 30 + ['Waiting for User'] * 15,
        'resolution_time_hours': list(np.random.randint(1, 50, 100)) + list(np.random.randint(50, 100, 50))
    }
    
    return pd.DataFrame(incidents_data), pd.DataFrame(tickets_data)

# Try to load real data, but fall back to demo data if it doesn't work
def try_load_real_data():
    """Try to load real data, but use demo data if it fails"""
    try:
        import sqlite3
        from pathlib import Path
        
        db_path = Path("DATA/intelligence_platform.db")
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            
            # Try to get real data
            incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
            tickets_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
            
            conn.close()
            
            if not incidents_df.empty and not tickets_df.empty:
                st.success("✅ Loaded your REAL Week 8 data!")
                return incidents_df, tickets_df, True
    except Exception as e:
        st.write(f"Note: {e}")
    
    # If we get here, use demo data
    incidents_df, tickets_df = create_demo_data()
    st.info("📝 Using demo data. Run `python main.py` to see your real data!")
    return incidents_df, tickets_df, False

# Load the data
incidents_df, tickets_df, is_real_data = try_load_real_data()

# Show what we're working with
st.header("📈 Data Overview")
col1, col2 = st.columns(2)

with col1:
    st.metric("Cyber Incidents", len(incidents_df))
    st.metric("Unique Severities", incidents_df['severity'].nunique())

with col2:
    st.metric("IT Tickets", len(tickets_df)) 
    st.metric("Ticket Priorities", tickets_df['priority'].nunique())

st.divider()

# Create charts section
st.header("📊 Creating Charts with Streamlit")

#Bar Charts
st.subheader("📊 Bar Charts")
st.write("Bar charts are great for comparing categories")

col1, col2 = st.columns(2)

with col1:
    st.write("**Cyber Incidents by Severity**")
    severity_counts = incidents_df['severity'].value_counts()
    st.bar_chart(severity_counts)

with col2:
    st.write("**IT Tickets by Priority**")
    priority_counts = tickets_df['priority'].value_counts()
    st.bar_chart(priority_counts)

#More bar charts
st.subheader("More Bar Charts")

col1, col2 = st.columns(2)

with col1:
    st.write("**Incidents by Category**")
    category_counts = incidents_df['category'].value_counts()
    st.bar_chart(category_counts)

with col2:
    st.write("**Tickets by Status**")
    status_counts = tickets_df['status'].value_counts()
    st.bar_chart(status_counts)

st.divider()

# Now we implement Line and Area Charts
st.header("📈 Line and Area Charts")
st.write("Line and area charts show trends over time")

# Create some time series data for line charts
dates = pd.date_range('2024-01-01', periods=50, freq='D')
line_data = pd.DataFrame({
    'date': dates,
    'value1': np.random.randn(50).cumsum() + 100,
    'value2': np.random.randn(50).cumsum() + 150,
    'value3': np.random.randn(50).cumsum() + 200
})

col1, col2 = st.columns(2)

with col1:
    st.write("**Line Chart - Multiple Series**")
    st.line_chart(line_data.set_index('date'))

with col2:
    st.write("**Area Chart - Single Series**")
    st.area_chart(line_data.set_index('date')['value1'])

st.divider()

#Advanced charts with real data
st.header("🎯 Advanced Chart Examples")

if is_real_data and 'resolution_time_hours' in tickets_df.columns:
    st.subheader("Real Data Analysis")
    
    # Resolution time analysis with my real data
    resolved_tickets = tickets_df[tickets_df['status'] == 'Resolved']
    if not resolved_tickets.empty:
        resolution_by_priority = resolved_tickets.groupby('priority')['resolution_time_hours'].mean()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Average Resolution Time by Priority**")
            st.bar_chart(resolution_by_priority)
        
        with col2:
            st.write("**Resolution Time Distribution**")
            st.area_chart(resolved_tickets['resolution_time_hours'].head(30))
    else:
        st.info("No resolved tickets in the data")
else:
    st.subheader("Demo Data Analysis")
    
    # Creating some interesting demo analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Demo: Incident Status by Severity**")
        demo_cross = pd.crosstab(incidents_df['severity'], incidents_df['status'])
        st.bar_chart(demo_cross)
    
    with col2:
        st.write("**Demo: Random Trend Data**")
        trend_data = pd.DataFrame({
            'trend': np.random.randn(30).cumsum() + 50
        })
        st.line_chart(trend_data)

st.divider()

# Section 5: Data tables
st.header("📋 View the Raw Data")

tab1, tab2 = st.tabs(["Cyber Incidents", "IT Tickets"])

with tab1:
    st.subheader("Cyber Incidents Data")
    st.dataframe(incidents_df.head(10))

with tab2:
    st.subheader("IT Tickets Data")
    st.dataframe(tickets_df.head(10))

st.success("🎉 I've learned how to create charts with Streamlit!")