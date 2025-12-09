import google.generativeai as genai

#Time to Configure Gemini
API_KEY = 'AIzaSyBg6VPnyNmYzEUTZLF3A5UQF8f1FE78IFA'
genai.configure(api_key=API_KEY)

# Initializing the model with system instructions
model = genai.GenerativeModel('gemini-1.5-flash')

print("Gemini AI Console Chat (type 'quit' to exit)")
print("-" * 50)

# Initializing conversation history
history = []

while True:
    # Getting user input
    user_input = input("You: ")
    
    # Exit condition
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    # Add user input to conversation
    history.append(f"User: {user_input}")
    
    # Build the conversation context
    conversation_context = "You are a helpful assistant.\n\n"
    conversation_context += "\n".join(history)
    conversation_context += "\nAssistant:"
    
    # Getting the  AI response
    response = model.generate_content(conversation_context)
    
    # Extracting and displaying response
    assistant_response = response.text
    print(f"AI: {assistant_response}\n")
    
    # Add assistant response to history
    history.append(f"Assistant: {assistant_response}")