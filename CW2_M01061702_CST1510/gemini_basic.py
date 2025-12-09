import google.generativeai as genai

# Configure Gemini
API_KEY = 'AIzaSyBg6VPnyNmYzEUTZLF3A5UQF8f1FE78IFA'  #My API KEY
genai.configure(api_key=API_KEY)

# Initializing the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Making a simple API call
response = model.generate_content("Hello! What is AI?")
print(response.text)
