import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
@st.cache_resource
def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        st.error("Supabase URL or Key is missing in environment variables.")
        st.stop()
    return create_client(url, key)

supabase = get_supabase_client()

def login_signup_ui():
    st.title("🐍 Python ChatBuddy")
    st.markdown("Please log in or sign up to access your interactive Python tutor.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to your account")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            try:
                response = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                if response.user:
                    st.session_state["user"] = response.user
                    st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

    with tab2:
        st.subheader("Create a new account")
        signup_email = st.text_input("Email", key="signup_email")
        signup_name = st.text_input("Name", key="signup_name")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Sign Up", key="signup_btn"):
            try:
                # Sign up
                response = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                if response.user:
                    # Create profile
                    supabase.table("profiles").insert({
                        "id": response.user.id,
                        "email": signup_email,
                        "name": signup_name
                    }).execute()
                    
                    st.success("Signup successful! You can now log in.")
            except Exception as e:
                st.error(f"Signup failed: {str(e)}")

def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state["user"] = None
    if "current_chat_id" in st.session_state:
        del st.session_state["current_chat_id"]
    if "messages" in st.session_state:
        st.session_state["messages"] = []
    st.rerun()

def get_current_user():
    return st.session_state.get("user")
