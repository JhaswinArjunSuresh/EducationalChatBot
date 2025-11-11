import fitz  # PyMuPDF
import numpy as np
import faiss
from typing import List, Tuple


class PDFVectorizerUnstructured:
    def __init__(self, embedder, indexer=None):
        self.embedder = embedder
        self.indexer = indexer
        self.texts = []
        self.metadata = []

    def extract_text(self, pdf_path: str) -> List[str]:
        """Extracts text from each page of a PDF."""
        doc = fitz.open(pdf_path)
        pages_text = [page.get_text("text").strip() for page in doc if page.get_text("text").strip()]
        return pages_text

    # def process_pdf(self, pdf_path: str):
    #     """Extracts text and builds a FAISS index."""
    #     texts = self.extract_text(pdf_path)
    #     if not texts:
    #         return None, [], []

    #     print("📄 Extracted", len(texts), "pages from PDF")

    #     # Create embeddings
    #     embeddings = self.embedder.encode(texts)
    #     vectors = np.array(embeddings).astype("float32")

    #     # Initialize FAISS index
    #     dim = vectors.shape[1]
    #     if self.indexer is None:
    #         self.indexer = faiss.IndexFlatL2(dim)
    #     self.indexer.add(vectors)

    #     self.texts = texts
    #     self.metadata = [{} for _ in texts]
    #     return self.indexer, texts, self.metadata
    def process_pdf(self, pdf_path):
        texts = self.extract_text(pdf_path)
        if not texts:
            return [], []

        embeddings = self.embedder.encode(texts)
        metadata = [{} for _ in texts]  # keep metadata placeholder

        return embeddings, texts, metadata


    def query_index(self, query, index, texts, metadata, base_k=5):
        """Retrieve top-k most relevant chunks for a query."""
        query_emb = self.embedder.encode([query])
        import numpy as np
        D, I = index.search(np.array(query_emb).astype("float32"), base_k)
        results = []
        for rank, idx in enumerate(I[0]):
            results.append({
                "rank": rank + 1,
                "text": texts[idx],
                "metadata": metadata[idx] if metadata else {}
            })
        return results

