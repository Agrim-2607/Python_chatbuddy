from auth import supabase
from datetime import datetime

def create_chat(user_id: str, title: str) -> str:
    response = supabase.table("chats").insert({"user_id": user_id, "title": title}).execute()
    if response.data:
        return response.data[0]["id"]
    return None

def get_user_chats(user_id: str) -> list:
    response = supabase.table("chats").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
    return response.data if response.data else []

def rename_chat(chat_id: str, new_title: str):
    supabase.table("chats").update({"title": new_title}).eq("id", chat_id).execute()

def delete_chat(chat_id: str):
    supabase.table("chats").delete().eq("id", chat_id).execute()

def save_message(chat_id: str, role: str, content: str):
    supabase.table("messages").insert({"chat_id": chat_id, "role": role, "content": content}).execute()
    # Assuming 'now()' is not evaluated by supabase python client in updates directly, we pass python datetime
    supabase.table("chats").update({"updated_at": datetime.now().isoformat()}).eq("id", chat_id).execute()

def get_chat_messages(chat_id: str) -> list:
    response = supabase.table("messages").select("*").eq("chat_id", chat_id).order("created_at", desc=False).execute()
    return response.data if response.data else []

def save_document(user_id: str, file_name: str, extracted_text: str) -> str:
    response = supabase.table("documents").insert({
        "user_id": user_id, 
        "file_name": file_name, 
        "extracted_text": extracted_text
    }).execute()
    if response.data:
        return response.data[0]["id"]
    return None
