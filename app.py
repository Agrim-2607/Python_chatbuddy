import streamlit as st
import os
from dotenv import load_dotenv

from auth import login_signup_ui, logout, get_current_user
from database import create_chat, get_user_chats, rename_chat, delete_chat, save_message, get_chat_messages, save_document
from gemini_client import GeminiClient
from document_processor import extract_text_from_file

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Python ChatBuddy", page_icon="🐍", layout="wide")

# Ensure required env variables
if not os.environ.get("GENAI_API_KEY"):
    st.error("Missing GENAI_API_KEY in environment variables.")
    st.stop()

# Authentication
user = get_current_user()
if not user:
    login_signup_ui()
    st.stop()

# --- Initialize session state ---
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_context" not in st.session_state:
    st.session_state.document_context = None

def start_new_chat():
    st.session_state.current_chat_id = None
    st.session_state.messages = []
    st.session_state.document_context = None

def load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    db_messages = get_chat_messages(chat_id)
    st.session_state.messages = [{"role": msg["role"], "content": msg["content"]} for msg in db_messages]

# --- Sidebar ---
with st.sidebar:
    st.title("🐍 Python ChatBuddy")
    st.markdown(f"Welcome, **{user.user_metadata.get('name', 'User')}**")
    
    with st.expander("⚙️ Settings"):
        st.write("Profile Settings")
        if st.button("Logout", use_container_width=True):
            logout()
            
    st.markdown("---")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        start_new_chat()
        st.rerun()

    st.subheader("Saved Chats")
    chats = get_user_chats(user.id)
    
    for chat in chats:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(chat["title"], key=f"chat_{chat['id']}", use_container_width=True):
                load_chat(chat["id"])
                st.rerun()
        with col2:
            with st.popover("⋮"):
                new_title = st.text_input("Rename", value=chat["title"], key=f"ren_{chat['id']}")
                if st.button("Save", key=f"save_{chat['id']}"):
                    rename_chat(chat["id"], new_title)
                    st.rerun()
                if st.button("Delete", key=f"del_{chat['id']}", type="primary"):
                    delete_chat(chat["id"])
                    if st.session_state.current_chat_id == chat["id"]:
                        start_new_chat()
                    st.rerun()
                    
    st.markdown("---")
    st.subheader("📚 Current Session Data")
    uploaded_file = st.file_uploader("Upload a Python notes document", type=["txt", "pdf", "docx", "doc", "md", "rtf"])
    
    if st.button("Process Document", use_container_width=True):
        with st.spinner("Extracting text..."):
            if uploaded_file is not None:
                try:
                    text_content = extract_text_from_file(uploaded_file, uploaded_file.name)
                    st.session_state.document_context = text_content
                    save_document(user.id, uploaded_file.name, text_content)
                    st.success("Document processed successfully.")
                except Exception as e:
                    st.error(f"Failed to read file: {e}")
            else:
                st.warning("Please upload a file first.")

# --- Main Chat Area ---
if st.session_state.document_context:
    st.info("📄 A document is currently loaded in context.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a Python question..."):
    # Create a new chat if it's the first message
    if st.session_state.current_chat_id is None:
        title = prompt[:30] + "..." if len(prompt) > 30 else prompt
        chat_id = create_chat(user.id, title)
        st.session_state.current_chat_id = chat_id

    # Add user message to state and db
    st.session_state.messages.append({"role": "user", "content": prompt})
    if st.session_state.current_chat_id:
        save_message(st.session_state.current_chat_id, "user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chatbot = GeminiClient()
                
                # Get response using context and history
                chat_history = st.session_state.messages[:-1] 
                
                response_text = chatbot.generate_response(
                    query=prompt, 
                    chat_history=chat_history,
                    document_context=st.session_state.document_context
                )
                
                st.markdown(response_text)
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                if st.session_state.current_chat_id:
                    save_message(st.session_state.current_chat_id, "assistant", response_text)
                    
            except Exception as e:
                st.error(f"Error: {e}")
