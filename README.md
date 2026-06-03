# Python ChatBuddy 🐍

A smart, Python-specific AI tutor chatbot built with Streamlit, Google GenAI SDK, FAISS, and Sentence Transformers. It uses a Retrieval-Augmented Generation (RAG) pipeline to learn from custom `.txt` files containing Python notes.

## 🚀 How to Run the App

1. **Prerequisites**: Make sure you have Python installed.
2. **Install Requirements**:
   Open a terminal in the `Python_chatbuddy` folder and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Streamlit**:
   Start the application by running:
   ```bash
   streamlit run app.py
   ```
   This will open the app in your default web browser.

## 🔑 Where and How to Put the API Key

You need a Google GenAI API Key to use this chatbot.

### How to Find Your API Key
1. Go to Google AI Studio: https://aistudio.google.com/app/apikey
2. Sign in with your Google Account.
3. Click on "Create API key" and copy the generated key.

### How to Add the API Key to the App
You have three options:
1. **(Easiest) In the App UI**: Simply paste the API key into the sidebar when you run the Streamlit app.
2. **Environment Variable (.env)**: Rename `.env.example` to `.env` and replace `your_api_key_here` with your actual key:
   ```env
   GENAI_API_KEY=AIzaSy...
   ```
3. **System Environment Variables**: Set `GENAI_API_KEY` in your system environment variables.

## 📄 How to Upload Your Text File

1. Run the app (`streamlit run app.py`).
2. Look at the left sidebar under **📚 Knowledge Base**.
3. Click "Browse files" or drag and drop your Python notes `.txt` file into the uploader.
4. Click the **Process Document** button. 
5. Wait for the success message confirming your document was chunked and indexed. 
   *(Note: If you don't upload a file, clicking "Process Document" will automatically load the default `data/python.txt` file provided in the repository.)*

## 🧠 How the Chatbot Pipeline Works (RAG)

This chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline:

1. **Document Loading & Chunking**: When you process a document, the `utils/document_loader.py` reads the text and splits it into smaller, overlapping chunks (about 800 characters each).
2. **Embeddings & Vector Store**: `utils/vector_store.py` takes these text chunks and converts them into numerical vectors (embeddings) using a lightweight local `sentence-transformers` model. These vectors are stored in a highly efficient local `FAISS` index.
3. **Retrieval**: When you ask a question, your query is also converted into a vector. FAISS searches the index to find the top 4 most relevant text chunks from your document.
4. **Generation**: `utils/chatbot.py` takes these retrieved chunks and your chat history, and securely sends them to the Gemini model using the latest `google.genai` SDK. The model is given strict system instructions to act as a Python tutor and base its answer on the retrieved context.
