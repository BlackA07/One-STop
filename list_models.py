import google.generativeai as genai

# --- Configuration ---
# 1. Paste the SAME API key you are using now
GOOGLE_API_KEY = 'AIzaSyBQ3q7XhOJF_try80r5WcVaCNmrH09Ix4E'

# 2. Setup the AI model
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error configuring API: {e}")
    exit()

print("--- Listing all available models for your API key ---")
print("Models that support 'generateContent':\n")

try:
    # This loop goes through every model the API knows about
    for m in genai.list_models():
        # We check if the model supports the 'generateContent' method (what we need)
        if 'generateContent' in m.supported_generation_methods:
            # If it does, we print its name
            print(m.name)
            
except Exception as e:
    print(f"\nAn error occurred while fetching models: {e}")
    print("This likely means your API key is invalid or has permissions issues.")

print("\n--- End of List ---")