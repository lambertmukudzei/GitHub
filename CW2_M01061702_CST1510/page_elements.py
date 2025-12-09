# This py file shows text, data, and images in Streamlit

import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Firstly we Set up the page
st.set_page_config(page_title="Page Elements Demo", page_icon="📄")

st.title("1. Basic Page Elements")
st.write("Now I'm learning how to show different types of content in Streamlit")

# Section 1: Headers and text
st.header("Headers and Text Elements")
st.subheader("This is a subheader")
st.caption("This is small caption text - good for explanations")
st.write("`st.write` is super flexible - it can show text, numbers, dataframes, anything!")
st.text("This is plain fixed-width text, good for showing code examples")
st.markdown("You can use **Markdown** here! *Italic text* and `code blocks` work too.")
st.markdown("> This is a blockquote - useful for important notes")

st.divider()  # Makes a nice separation line

# Section 2: Display data from MY Week 8 database
st.header("Display Data from My Database")
st.write("This is real data from my Week 8 project!")

# Connect to my database
def connect_database():
    db_path = Path("DATA") / "intelligence_platform.db"
    return sqlite3.connect(str(db_path))

# Get some cyber incidents from my database
conn = connect_database()
cyber_incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents LIMIT 10", conn)
conn.close()

st.write("Here are the first 10 cyber incidents from my database:")
st.dataframe(cyber_incidents_df)  # This makes a nice scrollable, sortable table

# Shows some statistics about my data
st.write("Quick stats about my cyber incidents:")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Incidents", "115")
with col2:
    st.metric("Different Severities", "4 types")
with col3:
    st.metric("Categories", "5 types")

st.divider()

# Section 3: Images
st.header("Images")
st.write("You can show images from URLs or local files")

# Show the Streamlit logo
st.image(
    "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png",
    caption="Streamlit Logo - this is from a URL",
    width=300
)

# Show a success message
st.success("Great! I learned how to display text, data, and images!")