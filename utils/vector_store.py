import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the vector store with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        
    def build_index(self, chunks: list[str]):
        """Builds the FAISS index from a list of text chunks."""
        self.chunks = chunks
        if not chunks:
            self.index = None
            return
            
        # Generate embeddings
        embeddings = self.model.encode(chunks, show_progress_bar=False)
        
        # Convert to numpy array of float32
        embeddings = np.array(embeddings).astype('float32')
        
        # Create FAISS index (L2 distance)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
    def search(self, query: str, k: int = 3) -> list[str]:
        """Searches for the top-k most relevant chunks for a given query."""
        if self.index is None or not self.chunks:
            return []
            
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        # Search FAISS
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])
                
        return results
