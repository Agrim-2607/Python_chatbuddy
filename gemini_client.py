import os
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GENAI_API_KEY")
        if not api_key:
            raise ValueError("GENAI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_response(self, query: str, chat_history: list = None, document_context: str = None) -> str:
        system_instruction = """You are Python ChatBuddy, a friendly but focused Python tutor. 
Help students learn Python through explanations, examples, debugging. 
You can answer general greetings normally and politely, but if the user asks completely unrelated non-Python things, gently redirect them back to Python.
"""
        if document_context:
            system_instruction += f"\nUse the following extracted document context whenever available to answer the user's question:\n<context>\n{document_context}\n</context>\n"

        contents = []
        if chat_history:
            for msg in chat_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
                
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
