import os
import io

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from striprtf.striprtf import rtf_to_text
except ImportError:
    rtf_to_text = None

def extract_text_from_file(file_obj, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in [".txt", ".md"]:
        return file_obj.read().decode("utf-8", errors="replace")
        
    elif ext == ".pdf":
        if not PdfReader:
            raise ImportError("pypdf is required to read .pdf files.")
        reader = PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            raise ValueError("No text could be extracted from this PDF. It might be a scanned image.")
        return text
        
    elif ext == ".docx":
        if not Document:
            raise ImportError("python-docx is required to read .docx files.")
        doc = Document(file_obj)
        return "\n".join([para.text for para in doc.paragraphs])
        
    elif ext == ".rtf":
        if not rtf_to_text:
            raise ImportError("striprtf is required to read .rtf files.")
        content = file_obj.read().decode("utf-8", errors="ignore")
        return rtf_to_text(content)
        
    elif ext == ".doc":
        raise ValueError("Older .doc files are not supported natively. Please resave the file as a .docx or .pdf in Word and upload it again.")
        
    else:
        raise ValueError(f"Unsupported file format: {ext}")
