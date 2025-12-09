#CST1510 Data Management dashboard
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path 
st.set_page_config(
    page_title="Data Management",
    page_icon="📊",
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
def load_datasets_data():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df

# Page header
st.title("Data Management Dashboard")
st.write(f"Managing datasets for {st.session_state.username}")

# Navigation tool
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    st.write(f"**Viewing:** Dataset Management")
with col3:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.divider()

# Load data
datasets_df = load_datasets_data()

# Metrics
st.header("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_datasets = len(datasets_df)
    st.metric("Total Datasets", total_datasets)

with col2:
    total_rows = datasets_df['rows'].sum()
    st.metric("Total Rows", f"{total_rows:,}")

with col3:
    avg_rows = datasets_df['rows'].mean()
    st.metric("Avg Rows/Dataset", f"{avg_rows:,.0f}")

with col4:
    total_columns = datasets_df['columns'].sum() if 'columns' in datasets_df.columns else 0
    st.metric("Total Columns", f"{total_columns:,}")

# Dataset visualization
st.header("Dataset Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dataset Sizes (Rows)")
    dataset_sizes = datasets_df.set_index('name')['rows']
    st.bar_chart(dataset_sizes)
    
    st.subheader("Uploaded By")
    if 'uploaded_by' in datasets_df.columns:
        uploader_counts = datasets_df['uploaded_by'].value_counts()
        st.bar_chart(uploader_counts)

with col2:
    st.subheader("Dataset Columns")
    if 'columns' in datasets_df.columns:
        dataset_columns = datasets_df.set_index('name')['columns']
        st.bar_chart(dataset_columns)
    
    #This Upload dates if available
    if 'upload_date' in datasets_df.columns:
        st.subheader("Upload Timeline")
        # Simple chart showing upload order
        st.line_chart(datasets_df['rows'])

# Dataset details
st.header("Dataset Details")
st.dataframe(datasets_df, use_container_width=True)

# Data statistics
st.header("Detailed Statistics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Row Statistics")
    row_stats = datasets_df['rows'].describe()
    st.write(row_stats)
    
    st.metric("Largest Dataset", f"{datasets_df['rows'].max():,} rows")
    st.metric("Smallest Dataset", f"{datasets_df['rows'].min():,} rows")

with col2:
    if 'columns' in datasets_df.columns:
        st.subheader("Column Statistics")
        col_stats = datasets_df['columns'].describe()
        st.write(col_stats)
        
        st.metric("Most Columns", datasets_df['columns'].max())
        st.metric("Fewest Columns", datasets_df['columns'].min())

# Footer
st.divider()
st.caption(f"Showing {len(datasets_df)} datasets from Week 8 database")
st.caption("Real dataset metadata from my project")
