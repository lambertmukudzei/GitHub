# 3_Data_Science.py
# Student ID: M01061702
# This is my Data Science Dashboard page, it shows all my datasets

# Importing libraries
import streamlit as st  # For building the web page
import pandas as pd  # For working with data tables
from services.database_manager import DatabaseManager  # My database connection

# SETTING UP THE PAGE
st.set_page_config(
    page_title="CST1510 Data Science Dashboard",  # Browser tab title
    page_icon="📊",  # Chart emoji in browser tab
    layout="wide"  # Makes page use full screen width
)

# This is a security check to make sure the user is logged in
# This prevents people from accessing the page without logging in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to access this page!")  # Shows warning
    if st.button("Go to Login"):  # Button to go to login
        st.switch_page("pages/1_Login.py")  # Takes user back to login
    st.stop()  # Stops code here can't see page without login

#The page header displayed at the top
col1, col2 = st.columns([3, 1])  # Creates two columns
with col1:  # Left column 
    st.title("CST1510 Data Science Dashboard")  # Main title 
    st.write(f"Welcome, **{st.session_state.username}**!")  # Personalized greeting
with col2:  # Right column 
    if st.button("Logout"): # Logout button
        # Clear all user data from memory
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.current_user = None
        st.switch_page("pages/1_Login.py")  # Go back to login

# CONNECTING TO DATABASE
@st.cache_resource  # Caches this, IT only connects once even if page refreshes
def get_db_manager():
    return DatabaseManager()  # Creates database connection object

db_manager = get_db_manager()  # Actually makes the connection

#the main conetent of my page
st.subheader("Datasets Overview")  # Section title

#Actaully getting the data from the database 
# Fetch all records from the datasets_metadata table
datasets_data = db_manager.fetch_all("SELECT * FROM datasets_metadata")

# Check if we got any data
if datasets_data:
    # Convert to a pandas dataframe (Like an excel TABLE)
    df = pd.DataFrame(datasets_data, columns=[
        'dataset_id', 'name', 'rows', 'columns', 
        'uploaded_by', 'upload_date', 'created_at'
    ])
    
    # Creating metrics table (TOP OF PAGE)
    col1, col2, col3 = st.columns(3)  # 3 equal columns for metrics
    with col1:
        total_rows = df['rows'].sum()  # Add up all rows from all datasets
        st.metric("Total Rows", f"{total_rows:,}")  # Format with commas (1,000)
    with col2:
        total_datasets = len(df)  # Count number of datasets
        st.metric("Total Datasets", total_datasets)
    with col3:
        avg_rows = df['rows'].mean()  # Calculate average rows per dataset
        st.metric("Avg Rows per Dataset", f"{avg_rows:,.0f}")  # Format without decimals
    
    st.divider()  # Horizontal line
    
    # Displaying the datasets table
    st.subheader(f"Available Datasets ({len(df)} total)")  # Shows count
    st.dataframe(
        df[['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date']],
        use_container_width=True  # Makes table use full width
    )
    
    # DATASET DETAILS SECTION
    st.subheader("Dataset Details")
    # Let user select which datasets to see more info about
    selected_ids = st.multiselect(
        "Select datasets to view details:",
        options=df['dataset_id'].tolist()  # List of all dataset IDs
    )
    
    # If user selected any datasets
    if selected_ids:
        for dataset_id in selected_ids:
            # Get the row for this dataset ID
            dataset_row = df[df['dataset_id'] == dataset_id].iloc[0]
            # Create expandable section (click to open)
            with st.expander(f"Dataset #{dataset_id} - {dataset_row['name']}"):
                # Show all details about this dataset
                st.write(f"**Name:** {dataset_row['name']}")
                st.write(f"**Rows:** {dataset_row['rows']:,}")  # Format with commas
                st.write(f"**Columns:** {dataset_row['columns']}")
                st.write(f"**Uploaded by:** {dataset_row['uploaded_by']}")
                st.write(f"**Upload date:** {dataset_row['upload_date']}")
                st.write(f"**Created at:** {dataset_row['created_at']}")
    
    # STATS SECTION
    st.subheader(" Dataset Statistics")
    col1, col2 = st.columns(2)  # Two columns for different charts/stats
    with col1:
        # Bar chart showing number of rows in each dataset
        # Sets dataset names as labels and row counts as values
        st.bar_chart(df.set_index('name')['rows'])
    with col2:
        st.write("**Dataset Sizes by Uploader:**")
        # Group datasets by who uploaded them, sum their rows
        uploader_stats = df.groupby('uploaded_by')['rows'].sum()
        # Display as a table
        st.dataframe(uploader_stats)
    
else:  # If no data in database
    st.info("No datasets found in the database.")

# SIDEBAR navigation
with st.sidebar:  # Everything here goes in the sidebar
    st.header("Navigation")
    st.write("Navigate to other domains:")
    
    # Navigation buttons in two columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cybersecurity"):
            st.switch_page("pages/2_Cyber_Security.py")
    with col2:
        if st.button("IT Operations"):
            st.switch_page("pages/4_IT_Operations.py")
    
    # AI Assistant button
    if st.button("AI Assistant"):
        st.switch_page("pages/5_AI_Assistant.py")
    
    st.divider()  # Horizontal line
    st.caption("CST1510 Data Science Dashboard-M01061702")  # Footer with my ID
# End of my code