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


def load_text_file(filepath: str) -> str:
    """Reads a text file and returns its content."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_file(file_obj, filename: str) -> str:
    """Extracts text from various file formats."""
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
        raise ValueError("Older .doc files are not supported. Please resave the file as a .docx or .pdf in Word and upload it again.")
        
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """
    Splits text into chunks of maximum `chunk_size` characters, 
    with `chunk_overlap` characters of overlap between consecutive chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        # Try to find a natural breaking point (newline or space) to avoid cutting words
        if end < text_length:
            newline_pos = text.rfind('\n', start, end)
            if newline_pos != -1 and newline_pos > start + chunk_size // 2:
                end = newline_pos + 1
            else:
                space_pos = text.rfind(' ', start, end)
                if space_pos != -1 and space_pos > start + chunk_size // 2:
                    end = space_pos + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        start = end - chunk_overlap
        # Prevent infinite loop if overlap is too large or we didn't advance
        if start < end - chunk_size + 1:
             start = end
             
    return chunks
