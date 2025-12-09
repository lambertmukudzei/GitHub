# This is my Streamlit layout practice file - learning how to organize dashboards
import streamlit as st  # Main library for web app
import pandas as pd  # For data tables
import numpy as np  # For math and random numbers

# We start off with page configuration
st.set_page_config(
    page_title="Layout Demo - My Dashboard",  # Browser tab title
    page_icon="📐",  # Ruler emoji for tab
    layout="wide"  # Use full screen width
)

# Main page title
st.title("Layout Demo")
st.write("Learning how to organize my Streamlit app")

# SIDEBAR (appears on left side)
with st.sidebar:
    st.header("My Controls")
    st.write("This sidebar is perfect for filters and controls!")
    
    # Dropdown menu to choose chart type
    chart_style = st.selectbox(
        "Choose chart style:",
        ["Bar Chart", "Line Chart", "Area Chart", "Scatter Chart"]
    )
    
    # Slider to choose how much data to show
    data_size = st.slider(
        "Number of data points:",
        min_value=10,
        max_value=200,
        value=50  # Default value
    )
    
    # Checkboxes to show/hide sections
    show_stats = st.checkbox("Show statistics", value=True)
    show_raw_data = st.checkbox("Show raw data", value=False)
    
    st.divider()  # Horizontal line
    st.write("**My Week 7 & 8 Project**")
    st.write("CST1510 - Multi-Domain Intelligence Platform")

# MAIN CONTENT AREA (right side of sidebar)
st.header("CST1510 Data Dashboard")

# Create sample sales data (like fake business data)
np.random.seed(42)  # Makes random numbers same every time (for testing)
sample_data = pd.DataFrame({
    'Month': [f'Month {i+1}' for i in range(12)],  # Months 1-12
    'Sales': np.random.randint(100, 500, 12),  # Random sales numbers
    'Customers': np.random.randint(50, 200, 12),  # Random customer counts
    'Revenue': np.random.randint(1000, 5000, 12)  # Random revenue
})

# Create dynamic data based on user's slider choice
dynamic_data = pd.DataFrame({
    'x': range(data_size),  # X values from 0 to data_size
    'value': np.random.randn(data_size).cumsum() + 100,  # Random trend
    'trend': np.arange(data_size) * 0.5 + np.random.randn(data_size)  # Another trend
})

# TOP METRICS ROW (4 boxes at top)
st.subheader("Key Metrics")

# Create 4 equal columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${sample_data['Sales'].sum():,}")  # Format with commas

with col2:
    st.metric("Average Customers", f"{sample_data['Customers'].mean():.0f}")  # No decimals

with col3:
    st.metric("Total Revenue", f"${sample_data['Revenue'].sum():,}")

with col4:
    # Calculate growth from first to last month
    growth = ((sample_data['Sales'].iloc[-1] - sample_data['Sales'].iloc[0]) / 
              sample_data['Sales'].iloc[0]) * 100
    st.metric("Growth", f"{growth:.1f}%")  # 1 decimal place

st.divider()  # Horizontal line

# CHARTS SECTION
st.header("Data Visualizations")

# Two main columns for charts
col1, col2 = st.columns(2)

with col1:  # Left chart (main chart)
    st.subheader("Main Chart")
    
    # Show different chart based on user selection
    if chart_style == "Bar Chart":
        st.bar_chart(sample_data.set_index('Month')['Sales'])
    elif chart_style == "Line Chart":
        st.line_chart(dynamic_data.set_index('x')['value'])
    elif chart_style == "Area Chart":
        st.area_chart(dynamic_data.set_index('x')['value'])
    else:  # Scatter Chart
        st.scatter_chart(dynamic_data, x='x', y='value', size='trend')
    
    st.write(f"Showing {data_size} data points as {chart_style}")

with col2:  # Right charts (supporting charts)
    st.subheader("Supporting Charts")
    
    # Two smaller charts
    st.bar_chart(sample_data.set_index('Month')['Customers'])
    st.write("Customer growth over time")
    
    st.line_chart(sample_data.set_index('Month')['Revenue'])
    st.write("Revenue trend")

# STATISTICS SECTION (only shows if checkbox is checked)
if show_stats:
    st.divider()
    st.header("Data Statistics")
    
    # Three columns for different stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Sales Stats")
        st.write(f"Mean: ${sample_data['Sales'].mean():.2f}")  # 2 decimals
        st.write(f"Median: ${sample_data['Sales'].median()}")
        st.write(f"Max: ${sample_data['Sales'].max()}")
    
    with col2:
        st.subheader("Customer Stats")
        st.write(f"Mean: {sample_data['Customers'].mean():.1f}")  # 1 decimal
        st.write(f"Median: {sample_data['Customers'].median()}")
        st.write(f"Max: {sample_data['Customers'].max()}")
    
    with col3:
        st.subheader("Revenue Stats")
        st.write(f"Mean: ${sample_data['Revenue'].mean():.2f}")
        st.write(f"Median: ${sample_data['Revenue'].median()}")
        st.write(f"Max: ${sample_data['Revenue'].max()}")

# RAW DATA SECTION (only shows if checkbox is checked)
if show_raw_data:
    st.divider()
    st.header("Raw Data")
    
    # Use expanders to save space (click to open)
    with st.expander("Click to view sample data"):
        st.dataframe(sample_data)  # Show the data table
        
        # Download button for the data
        st.download_button(
            label="Download data as CSV",
            data=sample_data.to_csv(index=False),  # Convert to CSV string
            file_name="my_sample_data.csv",
            mime="text/csv"
        )
    
    with st.expander("Click to view dynamic data"):
        st.dataframe(dynamic_data.head(20))  # Show first 20 rows

# FOOTER
st.divider()
st.success("You've mastered Streamlit layouts!")
st.info("""
**What I've learned:**
- Sidebars for controls
- Columns for organizing content  
- Metrics for key numbers
- Expandable sections
- Professional dashboard layout
""")