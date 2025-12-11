# MY 5_AI_Assistant.py
# This is my AI Assistant page, where there is a chatbot that can answer questions

# Importing libraries I need
import streamlit as st  # For building the web page
import os  # For working with operating system (like file paths)
import sys

# Clear cache to ensure fresh imports
st.cache_resource.clear()

# Add the parent directory to Python path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from services.ai_assistant import AIAssistant  # My custom AI assistant code

# Load environment variables from .env file ONCE at the beginning
load_dotenv()

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

# This is the header at the top of the page
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
@st.cache_resource(ttl=3600)  # Cache for 1 hour
def get_ai_assistant():
    # Get the API key from environment variables
    api_key = os.getenv("GOOGLE_API_KEY")  # Gets the API key from .env
    if not api_key:
        st.error("Google API Key not found. Please check your .env file.")
        st.stop()
    return AIAssistant(api_key=api_key)  # Creates AI assistant with the key

try:
    ai_assistant = get_ai_assistant()  # Actually creates the AI assistant
    
    # Debug: Check if method exists
    if not hasattr(ai_assistant, 'send_message'):
        st.error(f"ERROR: AIAssistant object has no 'send_message' method.")
        st.error(f"Available methods: {[m for m in dir(ai_assistant) if not m.startswith('_')]}")
        st.stop()
except Exception as e:
    st.error(f"Failed to create AI Assistant: {str(e)}")
    st.stop()

# The main chat interface
st.subheader("Chat with AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The input box where the user actually types their question
if prompt := st.chat_input("Ask me anything about intelligence domains..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ai_assistant.send_message(prompt)
                st.markdown(response)
            except Exception as e:
                error_msg = f"Error getting AI response: {str(e)}"
                st.error(error_msg)
                response = error_msg
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
