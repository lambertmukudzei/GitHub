# This is my AI Assistant - it talks to Google's Gemini AI
# Student ID: M01061702
import google.generativeai as genai
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

class AIAssistant:
    # My chatbot that connects to Google's AI
    
    def __init__(self, api_key: Optional[str] = None):
        # Load secret API key from .env file
        load_dotenv()
        
        # Try to get API key - from parameter or environment
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if self.api_key:  # If we have a key
            genai.configure(api_key=self.api_key)  # Connect to Google
            self.model = genai.GenerativeModel('gemini-pro')  # Use Gemini Pro
            self._history = []  # Store chat history
        else:
            self.model = None  # No AI without key
            print("Warning: No API key for AI Assistant")
    
    def set_system_prompt(self, prompt: str) -> None:
        # Tell AI what role to play
        self._history = [{"role": "user", "parts": prompt}]
    
    def send_message(self, user_message: str) -> str:
        # end question to AI, get answer back
        if not self.model:
            return "AI Assistant not set up. Need API key."
        
        try:
            response = self.model.generate_content(user_message)
            return response.text  # AI's response
        except Exception as e:
            return f"Error: {str(e)}"  # Show error if something breaks
    
    def clear_history(self) -> None:
        # Start new conversation
        self._history = []
    
    def analyze_security_incident(self, incident_description: str) -> str:
        #Ask AI to analyze security problem"""
        prompt = f"""
        As a cybersecurity expert, analyze:
        
        Incident: {incident_description}
        
        Provide:
        1. Severity assessment
        2. Immediate actions
        3. Prevention strategies
        4. Investigation tools
        """
        return self.send_message(prompt)  # Get AI's analysis
    
    def analyze_dataset(self, dataset_info: str) -> str:
        #Ask AI to analyze data
        prompt = f"""
        As a data scientist, analyze:
        
        {dataset_info}
        
        Provide:
        1. Potential insights
        2. Analysis techniques
        3. Data quality
        4. Visualization ideas
        """
        return self.send_message(prompt)  # Get AI's data insights