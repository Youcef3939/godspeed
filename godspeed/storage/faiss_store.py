from __future__ import annotations

from typing import List, Sequence

import faiss
import numpy as np

from godspeed.domain.models import Chunk, SearchHit


class FaissVectorStore:
    """Local FAISS-backed vector store; replaceable by distributed stores."""

    def __init__(self) -> None:
        self._index: faiss.Index | None = None
        self._chunks: List[Chunk] = []

    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        if not chunks:
            return
        matrix = np.asarray(embeddings, dtype="float32")
        if matrix.ndim != 2:
            raise ValueError("Embeddings should be a 2D array")
        if len(chunks) != matrix.shape[0]:
            raise ValueError("Chunks and embeddings size mismatch")

        if self._index is None:
            self._index = faiss.IndexFlatIP(matrix.shape[1])
        self._index.add(matrix)
        self._chunks.extend(chunks)

    def search(self, embedding: Sequence[float], top_k: int) -> Sequence[SearchHit]:
        if self._index is None or not self._chunks:
            return []
        query = np.asarray([embedding], dtype="float32")
        scores, indices = self._index.search(query, top_k)
        hits: List[SearchHit] = []
        for score, vector_index in zip(scores[0], indices[0]):
            if vector_index < 0:
                continue
            chunk = self._chunks[vector_index]
            hits.append(
                SearchHit(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    text=chunk.text,
                    score=float(score),
                    metadata=chunk.metadata,
                )
            )
        return hits
