import google.generativeai as genai
from dotenv import load_dotenv
import os

# Loading environment variables from .env file
load_dotenv()

# Getting API key from environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

# Configuring Gemini
genai.configure(api_key=API_KEY)

# Initializing the model
model = genai.GenerativeModel('gemini-1.5-flash')

print("Gemini AI Console Chat (type 'quit' to exit)")
print("-" * 50)

history = []

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    history.append(f"User: {user_input}")
    
    conversation_context = "You are a helpful assistant.\n\n"
    conversation_context += "\n".join(history)
    conversation_context += "\nAssistant:"
    
    response = model.generate_content(conversation_context)
    assistant_response = response.text
    print(f"AI: {assistant_response}\n")
    
    history.append(f"Assistant: {assistant_response}")