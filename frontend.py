import streamlit as st
import requests

st.title("📚 9th Class AI Assistant (Prototype)")

# Input
user_question = st.text_input("Ask a question from 9 Class Sindh Board Book:")

if st.button("Ask AI"):
    if user_question:
        with st.spinner("Thinking..."):
            # Connect to your running FastAPI
            try:
                response = requests.post("http://127.0.0.1:8001/ask", json={"question": user_question})
                if response.status_code == 200:
                    data = response.json()
                    st.success("Answer Found!")
                    st.write(data['answer'])
                    if data['context_found']:
                        st.info("Source: 9th Class Curriculum")
                    else:
                        st.warning("Source: General Knowledge (Not in books)")
                else:
                    st.error("Server Error")
            except:
                st.error("Could not connect to Backend. Is FastAPI running?")