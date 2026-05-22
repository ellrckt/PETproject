from sentence_transformers import SentenceTransformer
from typing import List
import logging

logger = logging.getLogger(__name__)

class ChatEmbeddingService:
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        logger.info(f" Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.dim = 384
        logger.info("Model loaded successfully")

    def embed_text(self, text: str) -> List[float]:
        if not text or len(text.strip()) < 2:
            return [0.0] * self.dim
            
        vector = self.model.encode(
            text,
            normalize_embeddings=True, 
            convert_to_numpy=True,
            show_progress_bar=False
        )
        return vector.tolist()

    # def embed_batch(self, texts: List[str]) -> List[List[float]]:
    #     if not texts:
    #         return []
    #     vectors = self.model.encode(
    #         texts,
    #         normalize_embeddings=True,
    #         convert_to_numpy=True,
    #         batch_size=32,
    #         show_progress_bar=False
    #     )
    #     return [v.tolist() for v in vectors]