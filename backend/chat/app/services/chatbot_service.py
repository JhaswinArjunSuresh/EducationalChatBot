import faiss
import numpy as np
import os
from threading import Lock
from chat.app.chatbot import CSVChatbot
from chat.app.embeddings.ollama_embedder import LocalOllamaEmbedder
from chat.app.pdf_embedder import PDFVectorizerUnstructured

class ChatbotService:
    _instance = None
    _initialized = False
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not ChatbotService._initialized:
            print("Initializing ChatbotService...")

            # Local Ollam for embeddings
            self.embedder = LocalOllamaEmbedder("mxbai-embed-large")  # or "nomic-embed-text"

            # PDF vectorizer
            self.vectorizer = PDFVectorizerUnstructured(self.embedder)

            # Chatbot for QA
            self.chatbot = CSVChatbot()

            # FAISS index
            self.index = None
            self.texts = []
            self.metadata = []

            # Build index automatically
            self.build_faiss_index_from_data()

            ChatbotService._initialized = True
            print("✅ ChatbotService initialized successfully.")

    def build_faiss_index_from_data(self):
        import faiss
        import numpy as np

        data_dir = "chat/data"
        pdf_files = [f for f in os.listdir(data_dir) if f.endswith(".pdf")]

        all_texts = []
        all_metadata = []
        all_vectors = []

        for pdf in pdf_files:
            path = os.path.join(data_dir, pdf)
            embeddings, texts, metadata = self.vectorizer.process_pdf(path)
            if embeddings is None or len(embeddings) == 0:
                continue

            all_texts.extend(texts)
            all_metadata.extend(metadata)
            all_vectors.extend(embeddings)

        if all_vectors:
            vectors = np.array(all_vectors).astype("float32")
            dim = vectors.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(vectors)
            self.texts = all_texts
            self.metadata = all_metadata
            print(f"✅ FAISS index built with {self.index.ntotal} vectors.")
        else:
            self.index = None
            self.texts = []
            self.metadata = []
            print("⚠️ No PDFs found or no text extracted.")


    def ask(self, query: str, k: int = 5) -> str:
        if self.index is None or self.index.ntotal == 0:
            return self.chatbot.generate_answer(query, "No data in the database.")
        results = self.vectorizer.query_index(query, self.index, self.texts, self.metadata, base_k=k)
        results_text = "\n\n".join([f"{r['rank']}. {r['text']}" for r in results])
        final_text = (
            f"Thinking - Content used for answering:\n\n"
            f"{results_text}\n\n"
            f"Chatbot Answer: \n\n"
            f"{self.chatbot.generate_answer(query, results_text)}"
        )
        return final_text

    def get_faiss_results(self, query: str, k: int = 5):
        if self.index is None or self.index.ntotal == 0:
            return []
        return self.vectorizer.query_index(query, self.index, self.texts, self.metadata, base_k=k)

chatbot_service = ChatbotService()

def ask(query: str, k: int = 5) -> str:
    return chatbot_service.ask(query, k)

def get_faiss_results(query: str, k: int = 5):
    return chatbot_service.get_faiss_results(query, k)

def rebuild_index():
    chatbot_service.build_faiss_index_from_data()
    return f"FAISS index rebuilt with {0 if chatbot_service.index is None else chatbot_service.index.ntotal} vectors."
