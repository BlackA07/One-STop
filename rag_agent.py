import sqlite3
import google.generativeai as genai

# --- Configuration ---
DATABASE_FILE = 'knowledge.db'

# 1. Paste your API key here
GOOGLE_API_KEY = 'AIzaSyBQ3q7XhOJF_try80r5WcVaCNmrH09Ix4E'

# 2. Setup the AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-pro')

# --- Part 1: The Retriever (Your old function) ---
def search_knowledge_base(query):
    """
    Searches the database for relevant text chunks.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    search_term = f"%{query}%"
    
    # We select the whole chunk
    cursor.execute(
        "SELECT text_chunk FROM knowledge WHERE text_chunk LIKE ?", 
        (search_term,)
    )
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        # Combine the text from all results
        # We'll just use the first result for this simple test
        return results[0][0]
    else:
        return None

# --- Part 2: The Generator (The new AI function) ---
def generate_answer(context, question):
    """
    Generates an answer using the AI model based on the context.
    """
    if context:
        # This is the "RAG" prompt.
        # It tells the AI to answer USING ONLY the provided text.
        prompt = f"""You are a helpful assistant for a 9th-class student.
        Answer the user's question **using only the following text**.
        Do not add any information from the internet.

        Source Text:
        "{context}"

        User's Question:
        "{question}"
        """
    else:
        # This is the "Fallback" prompt.
        # It's used when we find nothing in our database.
        prompt = f"""You are a helpful assistant. The user's question was not found in their 
        study notes. Please provide a general, helpful answer to their question:
        
        "{question}"
        """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Could not generate answer. {e}"


# --- Main Program: Run the RAG pipeline ---
if __name__ == '__main__':
    
    # --- Test with a question IN your database ---
    user_question_1 = "What is Biology?"
    
    print(f"--- Question 1: {user_question_1} ---")
    
    # 1. Retrieve
    print("Step 1: Searching database...")
    context = search_knowledge_base(user_question_1)
    
    # 2. Generate
    if context:
        print("Step 2: Found context. Generating answer...")
    else:
        print("Step 2: No context found. Using fallback...")
        
    answer_1 = generate_answer(context, user_question_1)
    print(f"\nAI Answer:\n{answer_1}\n")

    
    # --- Test with a question NOT in your database ---
    user_question_2 = "What is the capital of France?"
    
    print(f"--- Question 2: {user_question_2} ---")
    
    # 1. Retrieve
    print("Step 1: Searching database...")
    context_2 = search_knowledge_base(user_question_2)
    
    # 2. Generate
    if context_2:
        print("Step 2: Found context. Generating answer...")
    else:
        print("Step 2: No context found. Using fallback...")
        
    answer_2 = generate_answer(context_2, user_question_2)
    print(f"\nAI Answer:\n{answer_2}\n")