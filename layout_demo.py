import streamlit as st
import pandas as pd
import numpy as np

# We start off with page configuaration
st.set_page_config(
    page_title="Layout Demo - My Dashboard",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Layout Demo")
st.write("Learning how to organize my Streamlit app")

#SIDEBAR
with st.sidebar:
    st.header("🎛️ My Controls")
    st.write("This sidebar is perfect for filters and controls!")
    
    # Chart type selector
    chart_style = st.selectbox(
        "Choose chart style:",
        ["Bar Chart", "Line Chart", "Area Chart", "Scatter Chart"]
    )
    
    # Data size control
    data_size = st.slider(
        "Number of data points:",
        min_value=10,
        max_value=200,
        value=50
    )
    
    # Display options
    show_stats = st.checkbox("Show statistics", value=True)
    show_raw_data = st.checkbox("Show raw data", value=False)
    
    st.divider()
    st.write("**My Week 7 & 8 Project**")
    st.write("CST1510 - Multi-Domain Intelligence Platform")

#MAIN CONTENT
st.header("📊 My Data Dashboard")

# Create sample data based on user selection
np.random.seed(42)  # For consistent random data
sample_data = pd.DataFrame({
    'Month': [f'Month {i+1}' for i in range(12)],
    'Sales': np.random.randint(100, 500, 12),
    'Customers': np.random.randint(50, 200, 12),
    'Revenue': np.random.randint(1000, 5000, 12)
})

# Create dynamic data based on slider
dynamic_data = pd.DataFrame({
    'x': range(data_size),
    'value': np.random.randn(data_size).cumsum() + 100,
    'trend': np.arange(data_size) * 0.5 + np.random.randn(data_size)
})

#TOP METRICS ROW
st.subheader("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${sample_data['Sales'].sum():,}")

with col2:
    st.metric("Average Customers", f"{sample_data['Customers'].mean():.0f}")

with col3:
    st.metric("Total Revenue", f"${sample_data['Revenue'].sum():,}")

with col4:
    growth = ((sample_data['Sales'].iloc[-1] - sample_data['Sales'].iloc[0]) / sample_data['Sales'].iloc[0]) * 100
    st.metric("Growth", f"{growth:.1f}%")

st.divider()

#CHARTS SECTION
st.header("📊 Data Visualizations")

# Two main columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Main Chart")
    
    if chart_style == "Bar Chart":
        st.bar_chart(sample_data.set_index('Month')['Sales'])
    elif chart_style == "Line Chart":
        st.line_chart(dynamic_data.set_index('x')['value'])
    elif chart_style == "Area Chart":
        st.area_chart(dynamic_data.set_index('x')['value'])
    else:  # Scatter Chart
        st.scatter_chart(dynamic_data, x='x', y='value', size='trend')
    
    st.write(f"Showing {data_size} data points as {chart_style}")

with col2:
    st.subheader("Supporting Charts")
    
    # Mini charts in the right column
    st.bar_chart(sample_data.set_index('Month')['Customers'])
    st.write("Customer growth over time")
    
    st.line_chart(sample_data.set_index('Month')['Revenue'])
    st.write("Revenue trend")

#STATISTICS SECTION
if show_stats:
    st.divider()
    st.header("📋 Data Statistics")
    
    # Three columns for stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Sales Stats")
        st.write(f"Mean: ${sample_data['Sales'].mean():.2f}")
        st.write(f"Median: ${sample_data['Sales'].median()}")
        st.write(f"Max: ${sample_data['Sales'].max()}")
    
    with col2:
        st.subheader("Customer Stats")
        st.write(f"Mean: {sample_data['Customers'].mean():.1f}")
        st.write(f"Median: {sample_data['Customers'].median()}")
        st.write(f"Max: {sample_data['Customers'].max()}")
    
    with col3:
        st.subheader("Revenue Stats")
        st.write(f"Mean: ${sample_data['Revenue'].mean():.2f}")
        st.write(f"Median: ${sample_data['Revenue'].median()}")
        st.write(f"Max: ${sample_data['Revenue'].max()}")

#RAW DATA SECTION
if show_raw_data:
    st.divider()
    st.header("📄 Raw Data")
    
    # Use expanders to save space
    with st.expander("Click to view sample data"):
        st.dataframe(sample_data)
        
        # Download button
        st.download_button(
            label="Download data as CSV",
            data=sample_data.to_csv(index=False),
            file_name="my_sample_data.csv",
            mime="text/csv"
        )
    
    with st.expander("Click to view dynamic data"):
        st.dataframe(dynamic_data.head(20))

#FOOTER
st.divider()
st.success("🎉 You've mastered Streamlit layouts!")
st.info("""
**What I've learned:**
- Sidebars for controls
- Columns for organizing content  
- Metrics for key numbers
- Expandable sections
- Professional dashboard layout
""")