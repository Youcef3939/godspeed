from __future__ import annotations

from typing import Sequence

from godspeed.domain.models import SearchHit, SearchResponse
from godspeed.interfaces.contracts import Embedder, VectorStore


class Retriever:
    def __init__(self, embedder: Embedder, store: VectorStore) -> None:
        self.embedder = embedder
        self.store = store

    def search(self, query: str, top_k: int = 5) -> SearchResponse:
        query_vector = self.embedder.embed([query])[0]
        hits: Sequence[SearchHit] = self.store.search(query_vector, top_k=top_k)
        return SearchResponse(query=query, hits=list(hits))

