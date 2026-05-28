from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from godspeed.core.logging import configure_logging
from godspeed.embedding.sentence_transformer import SentenceTransformerEmbedder
from godspeed.ingestion.text_ingestor import TextDirectoryIngestor
from godspeed.pipeline import SearchPipeline
from godspeed.processing.chunker import FixedSizeChunkProcessor
from godspeed.storage.faiss_store import FaissVectorStore


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class QueryHit(BaseModel):
    rank: int
    score: float
    chunk_id: str
    doc_id: str
    citation: Dict[str, str]
    text: str


class QueryResponse(BaseModel):
    query: str
    hits: List[QueryHit]


def _build_pipeline() -> SearchPipeline:
    return SearchPipeline(
        ingestor=TextDirectoryIngestor(),
        processor=FixedSizeChunkProcessor(),
        embedder=SentenceTransformerEmbedder(),
        store=FaissVectorStore(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    pipeline = _build_pipeline()
    corpus_dir = os.getenv("GODSPEED_CORPUS_DIR")
    if corpus_dir:
        pipeline.index(corpus_dir)
    app.state.pipeline = pipeline
    yield


app = FastAPI(title="Godspeed Search API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    response = app.state.pipeline.query(payload.query, top_k=payload.top_k)
    hits = [
        QueryHit(
            rank=index + 1,
            score=hit.score,
            chunk_id=hit.chunk_id,
            doc_id=hit.doc_id,
            citation=hit.metadata,
            text=hit.text,
        )
        for index, hit in enumerate(response.hits)
    ]
    return QueryResponse(query=response.query, hits=hits)

