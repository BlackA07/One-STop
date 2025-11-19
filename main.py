from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
import google.generativeai as genai
import os

# --- Configuration ---
# Set up your API keys (use environment variables for security later)
SUPABASE_URL = "https://ifbknohkqfqplwvocksc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmYmtub2hrcWZxcGx3dm9ja3NjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4NjIyMjIsImV4cCI6MjA3NDQzODIyMn0.a5motl3g-arn6B-_JmL4J6WhmwacAkesfW1LnD52FQY"
GOOGLE_API_KEY = 'AIzaSyBQ3q7XhOJF_try80r5WcVaCNmrH09Ix4E'

# --- Initialize App and Clients ---
app = FastAPI()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-latest') # Or the model that worked for you

# This defines the data your app must send: {"question": "What is biology?"}
class UserQuery(BaseModel):
    question: str

# --- RAG Functions ---
def search_knowledge_base(query: str):
    """Searches the ONLINE Supabase DB for context."""
    print(f"Searching Supabase for: {query}")
    search_term = f"%{query}%"
    try:
        # Note: 'ilike' is a case-insensitive search
        data = supabase.table('knowledge').select('text_chunk').ilike('text_chunk', search_term).limit(1).execute()
        if data.data:
            return data.data[0]['text_chunk']
        else:
            return None
    except Exception as e:
        print(f"Supabase search error: {e}")
        return None

def generate_answer(context: str, question: str):
    """Generates an answer using the AI model."""
    if context:
        prompt = f"Using only this text: '{context}'. Answer this question: '{question}'"
    else:
        # The fallback prompt (we'll handle the "ask user" logic in Flutter)
        prompt = f"Provide a general, helpful answer to this question: '{question}'"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Could not generate answer. {e}"

# --- API Endpoint ---
# This is the URL your Flutter app will call
@app.post("/ask")
async def handle_question(query: UserQuery):
    """
    Main API endpoint to handle a user's question.
    """
    question = query.question
    print(f"Received question: {question}")

    # 1. Retrieve
    context = search_knowledge_base(question)

    # 2. Generate
    answer = generate_answer(context, question)

    # Send the answer back to the Flutter app
    return {"answer": answer, "context_found": (context is not None)}