from __future__ import annotations

from typing import Protocol, Sequence

from godspeed.domain.models import Chunk, Document, SearchHit


class Ingestor(Protocol):
    def ingest(self, source: str) -> Sequence[Document]:
        ...


class ChunkProcessor(Protocol):
    def split(self, documents: Sequence[Document]) -> Sequence[Chunk]:
        ...


class Embedder(Protocol):
    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        ...


class VectorStore(Protocol):
    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        ...

    def search(self, embedding: Sequence[float], top_k: int) -> Sequence[SearchHit]:
        ...

