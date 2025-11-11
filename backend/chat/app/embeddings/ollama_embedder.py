from langchain_ollama import OllamaEmbeddings

class LocalOllamaEmbedder:
    def __init__(self, model_name="mxbai-embed-large"):
        # You can use "nomic-embed-text" too if it's lighter
        self.model_name = model_name
        self.embeddings = OllamaEmbeddings(model=model_name)

    def encode(self, texts):
        """Generate embeddings for a list of text strings."""
        if isinstance(texts, str):
            texts = [texts]
        vectors = self.embeddings.embed_documents(texts)
        import numpy as np
        return np.array(vectors)
