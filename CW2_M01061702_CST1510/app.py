#M01061702 CST1510 - Streamlit App
# This is MY very first Streamlit app
import streamlit as st

# Setting up the page configurations - this makes it look nice
st.set_page_config(
    page_title="My First Streamlit App",
    page_icon="👋"
)

# This is the main title of the application
st.title("Hello, Streamlit! 👋")
st.write("This is my very first Streamlit app for my CST1510 project.")
st.write("I'm building this using what I learned in Week 7 and Week 8!")

# Now I must add some information about my project
st.divider()  # This makes a nice line to separate sections
st.header("About My Project")
st.write("**Week 7**: I built a secure authentication system with password hashing using the bcrypt hashing function")
st.write("**Week 8**: I created a SQLite database with cyber incidents, IT tickets, and datasets")

# Shows some basic data from my Week 8 database
st.divider()
st.header("My Database Stats")
st.write("In my database I have:")
st.write("- 🔐 115 cyber security incidents")
st.write("- 🎫 150 IT support tickets") 
st.write("- 📊 5 datasets with metadata")
st.write("- 👥 4 user accounts")

st.success("Success! My first Streamlit app is working!")