# MY 5_AI_Assistant.py
# This is my AI Assistant page, where there is a chatbot that can answer questions

# Importing libraries I need
import streamlit as st  # For building the web page
from services.ai_assistant import AIAssistant  # My custom AI assistant code
import os  # For working with operating system (like file paths)
from dotenv import load_dotenv  # For loading secret API keys from .env file

# setting up my page
st.set_page_config(
    page_title="My AI Assistant",  # Browser tab title
    page_icon="🤖",  # Robot emoji in browser tab
    layout="wide"  # Makes page use full screen width
)

# authentication check to make sure user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to access this page!")  # Warning message
    if st.button("Go to Login"):  # Button to go to login
        st.switch_page("pages/1_Login.py")  # Takes user back to login
    st.stop()  # Stops code here - can't see the page without login

#This is the header at the top of the page
col1, col2 = st.columns([3, 1])  # Two columns: big left (3/4), small right (1/4)
with col1:  # Left column
    st.title("🤖 AI Assistant")  # Main title with robot emoji
    st.write(f"Welcome, **{st.session_state.username}**!")  # Personalized greeting
    st.write("Ask questions about cybersecurity, data science, or IT operations.")  # Instructions
with col2:  # Right column
    if st.button("Logout"):  # Logout button
        # Clear all user data from memory
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.current_user = None
        st.switch_page("pages/1_Login.py")  # Go back to login

# setting up AI assistant
@st.cache_resource  # Only loads once even if page refreshes
def get_ai_assistant():
    load_dotenv()  # Loads secret keys from .env file (keeps API key hidden)
    api_key = os.getenv("GOOGLE_API_KEY")  # Gets the API key from .env
    return AIAssistant(api_key=api_key)  # Creates AI assistant with the key

ai_assistant = get_ai_assistant()  # Actually creates the AI assistant

# The main chat interface
st.subheader("💬 Chat with AI Assistant")#Added a chat emoji to add flair, In th Lab wew ere told we can use our own emoji's

# Initialize chat history (if it doesn't exist yet)
# Session state remembers conversation even if page refreshes
if "messages" not in st.session_state:
    st.session_state.messages = []  # Empty list to store messages

# Display previous chat messages (like looking at old texts)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Shows as user or assistant
        st.markdown(message["content"])  # Shows the message text

# The input box where the user actually types their question
# := is called "walrus operator" - assigns and checks at same time
if prompt := st.chat_input("Ask me anything about intelligence domains..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)  # Shows what user typed
    
    # Get AI response (this might take a few seconds)
    with st.chat_message("assistant"):  # Shows as AI assistant
        with st.spinner("Thinking..."):  # Shows loading spinner
            response = ai_assistant.send_message(prompt)  # Send to AI and get response
            st.markdown(response)  # Show AI's answer
    
    # Add AI response to chat history (so we remember the conversation)
    st.session_state.messages.append({"role": "assistant", "content": response})

# CLEAR CHAT BUTTON (START OVER)
if st.button("Clear Chat History"):
    st.session_state.messages = []  # Empty the messages list
    ai_assistant.clear_history()  # Also clear AI's memory of conversation
    st.rerun()  # Refresh page to show empty chat

# the predefined questions section
st.subheader("Quick Questions")
col1, col2, col3 = st.columns(3)  # 3 columns for quick questions

with col1:
    if st.button("Cybersecurity Best Practices"):
        with st.spinner("Getting answer..."):  # Shows loading
            # Ask AI a specific question
            response = ai_assistant.send_message(
                "What are the top 5 cybersecurity best practices for a small business?"
            )
            st.info(response[:200] + "...")  # Show first 200 characters

with col2:
    if st.button("Data Analysis Techniques"):
        with st.spinner("Getting answer..."):
            response = ai_assistant.send_message(
                "What are the most effective data analysis techniques for customer churn prediction?"
            )
            st.info(response[:200] + "...")

with col3:
    if st.button("IT Ticket Management"):
        with st.spinner("Getting answer..."):
            response = ai_assistant.send_message(
                "How can I improve IT ticket resolution times in a help desk environment?"
            )
            st.info(response[:200] + "...")

# API KEY CONFIGURATION SECTION (FOR SETUP HELP)
with st.expander("🔧 AI Assistant Configuration"):  # Click to expand
    st.write("**Current API Key Status:**")
    if ai_assistant.api_key:
        st.success("Succcess, API Key is configured")  #success message
    else:
        st.warning("Error, API Key not found")  # Yellow warning
        st.info("Set your Google API key in the `.env` file as `GOOGLE_API_KEY=your_key_here`")

# SIDEBAR NAVIGATION
with st.sidebar:  # Everything here goes in sidebar
    st.header("Navigation")
    st.write("Navigate to other domains:")
    
    # Navigation buttons in two columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cybersecurity"):
            st.switch_page("pages/2_Cyber_Security.py")
    with col2:
        if st.button("Data Science"):
            st.switch_page("pages/3_Data_Science.py")
    
    # IT Operations button
    if st.button("IT Operations"):
        st.switch_page("pages/4_IT_Operations.py")
    
    st.divider()  # Horizontal line
    
    # CHAT HISTORY IN SIDEBAR (SHOWS RECENT MESSAGES)
    st.subheader("Recent Chat")
    if st.session_state.messages:  # If there are messages
        # Show last 5 messages ([-5:] means last 5 items)
        for i, message in enumerate(st.session_state.messages[-5:]):
            role = "user" if message["role"] == "user" else "AI" 
            st.caption(f"{role} {message['content'][:50]}...")  # Show first 50 chars
    else:
        st.caption("No chat history yet")  # If no messages yet
    
    st.divider()  # Horizontal line
    st.caption("CST1510 AI Assistant")  # Footer
# End of my code