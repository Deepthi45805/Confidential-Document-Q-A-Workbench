from sentence_transformers import SentenceTransformer
from typing import List
from config.settings import EMBEDDING_MODEL_NAME

class EmbeddingManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls)
            cls._instance.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return cls._instance

    def embed_text(self, text: str) -> List[float]:
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
