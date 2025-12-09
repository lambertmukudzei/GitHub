import streamlit as st
import pandas as pd
import sqlite3
import bcrypt
from pathlib import Path

# First we Set up the page
st.set_page_config(
    page_title="Widgets Demo - My Week 7 & 8 Data",
    page_icon="🎛️",
    layout="centered"
)

st.title("Widgets Demo with My Real Data")
st.write("This shows my Week 7 authentication and Week 8 database!")

# Safe function to get data from database
def get_my_data():
    try:
        # Check if database exists
        db_path = Path("DATA/intelligence_platform.db")
        if not db_path.exists():
            return None, "Database not found. Run main.py first."
        
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        
        # Get some data samples
        users_df = pd.read_sql_query("SELECT username, role FROM users", conn)
        incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents LIMIT 5", conn)
        tickets_df = pd.read_sql_query("SELECT * FROM it_tickets LIMIT 5", conn)
        
        conn.close()
        return {"users": users_df, "incidents": incidents_df, "tickets": tickets_df}, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

#Week 7 Authentication Demo
st.header(" Week 7 Authentication Demo")
st.write("This uses my actual login system from Week 7!")

# Simple login form
username = st.text_input("Username", placeholder="Try: test_user")
password = st.text_input("Password", type="password", placeholder="Try: SecurePass123!")

if st.button("Test Login"):
    if username and password:
        try:
            # Check if user exists in database
            db_path = Path("DATA/intelligence_platform.db")
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()
                conn.close()
                
                if user:
                    # Verify password with bcrypt (Week 7)
                    stored_hash = user[2]
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                        st.success(f"✅ Login successful! Welcome {username}!")
                        st.balloons()
                    else:
                        st.error(" Wrong password!")
                else:
                    st.error(" User not found!")
            else:
                st.warning("Database not found - run main.py first")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter both username and password")

st.divider()

#Data exploration widgets
st.header("Explore My Week 8 Data")

# Gets the data
data, error = get_my_data()

if error:
    st.error(f"{error}")
    st.info("To see real data, make sure you've run: python main.py")
    
    # Show demo data instead
    st.subheader("Demo Data (for learning)")
    demo_df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['London', 'New York', 'Tokyo']
    })
    st.dataframe(demo_df)
    
else:
    st.success("Successfully loaded my real data!")
    
    # Show user data
    st.subheader("My Users")
    st.dataframe(data['users'])
    
    # Interactive selection
    st.subheader("Filter Cyber Incidents")
    severity_filter = st.selectbox(
        "Filter by severity:",
        ["All", "Critical", "High", "Medium", "Low"]
    )
    
    if severity_filter != "All":
        filtered = data['incidents'][data['incidents']['severity'] == severity_filter]
        st.write(f"Showing {len(filtered)} {severity_filter} incidents")
        st.dataframe(filtered)
    else:
        st.dataframe(data['incidents'])

st.divider()

#More interactive widgets
st.header("More Interactive Features")

# Number input example
age = st.number_input("How old are you?", min_value=0, max_value=120, value=25)
st.write(f"You are {age} years old")

# Slider example
rating = st.slider("How much do you like Streamlit?", 1, 10, 8)
st.write(f"You rated Streamlit: {rating}/10")

# Selectbox example
color = st.selectbox("Favorite color?", ["Red", "Blue", "Green", "Yellow", "Purple"])
st.write(f"Your favorite color is: {color}")

# Multiselect example
fruits = st.multiselect(
    "Select your favorite fruits:",
    ["Apple", "Banana", "Orange", "Grapes", "Strawberry"]
)
st.write(f"You selected: {', '.join(fruits) if fruits else 'No fruits'}")

# Checkbox example
agree = st.checkbox("I understand how widgets work")
if agree:
    st.info("Great! You're learning Streamlit!")

st.success("I've learned how to use widgets with Streamlit!")