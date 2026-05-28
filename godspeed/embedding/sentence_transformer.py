from __future__ import annotations
from typing import Sequence
from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        vectors = self.model.encode(list(texts), normalize_embeddings=True)
        return vectors.tolist()
