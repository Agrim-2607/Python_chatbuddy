try:
    import streamlit as st
except ImportError as e:
    import sys

    raise ImportError(
        "Failed to import streamlit. Are you running this script with the venv python?\n"
        f"Python executable: {sys.executable}\n"
        f"sys.path: {sys.path}\n"
    ) from e

import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Setup API
api_key = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=api_key)

# 1. LOAD YOUR KNOWLEDGE BASE
with open("python.txt", "r", encoding="utf-8") as f:
    python_docs = f.read()

# 2. DEFINE THE SYSTEM ROLE
system_prompt = f"""
You are an expert Python Programming Assistant. 
Use the following documentation as your primary knowledge base:
{python_docs}

STRICT RULES:
1. Only answer questions related to Python programming.
2. If the user asks about other topics, say: 'I am specifically trained to help with Python. Please ask a Python-related question.'
3. Be concise and use code examples where helpful.
"""

# 3. INITIALIZE THE MODEL WITH INSTRUCTIONS
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model='gemini-1.5-flash',
        config={'system_instruction': system_prompt}
    )

# Display Chat History
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User Input
if prompt := st.chat_input("Ask a Python question..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send message to Gemini chat session
    response = st.session_state.chat_session.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)