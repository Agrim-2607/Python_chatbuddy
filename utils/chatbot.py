import os
from google import genai
from google.genai import types

class PythonChatbot:
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("Google GenAI API Key is missing. Please provide it or set GENAI_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_response(self, query: str, context_chunks: list[str], chat_history: list = None) -> str:
        """
        Generates an answer using the retrieved context and chat history.
        """
        context_text = "\n\n---\n\n".join(context_chunks) if context_chunks else "No specific document context provided."
        
        system_instruction = f"""You are an expert Python Programming Assistant. 
        
Your primary knowledge base is the following context retrieved from the user's uploaded documents:
<context>
{context_text}
</context>

STRICT RULES:
1. Only answer questions related to Python programming.
2. If the user asks about other topics, politely decline and say: 'I am specifically trained to help with Python. Please ask a Python-related question.'
3. If the answer is found in the <context>, base your answer heavily on it.
4. Be concise, clear, and use code examples where helpful.
"""

        contents = []
        if chat_history:
            for msg in chat_history:
                # Map Streamlit roles to Gemini roles
                role = "user" if msg["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
                
        # Append the current query
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=query)]
            )
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3
                )
            )
            return response.text
        except Exception as e:
            return f"An error occurred while communicating with Gemini: {str(e)}"
