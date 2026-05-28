from __future__ import annotations

import logging
from typing import Sequence

from godspeed.domain.models import SearchResponse
from godspeed.interfaces.contracts import ChunkProcessor, Embedder, Ingestor, VectorStore
from godspeed.retrieval.retriever import Retriever

logger = logging.getLogger(__name__)


class SearchPipeline:
    """Coordinates ingest -> chunk -> embed -> index -> retrieve."""

    def __init__(
        self,
        ingestor: Ingestor,
        processor: ChunkProcessor,
        embedder: Embedder,
        store: VectorStore,
    ) -> None:
        self.ingestor = ingestor
        self.processor = processor
        self.embedder = embedder
        self.store = store
        self.retriever = Retriever(embedder=embedder, store=store)

    def index(self, source: str) -> int:
        documents = self.ingestor.ingest(source)
        chunks = self.processor.split(documents)
        embeddings: Sequence[Sequence[float]] = self.embedder.embed([c.text for c in chunks]) if chunks else []
        self.store.add(chunks, embeddings)
        logger.info("Indexed %d docs and %d chunks from %s", len(documents), len(chunks), source)
        return len(chunks)

    def query(self, query: str, top_k: int = 5) -> SearchResponse:
        response = self.retriever.search(query=query, top_k=top_k)
        logger.info("Retrieved %d hits for query: %s", len(response.hits), query)
        return response

