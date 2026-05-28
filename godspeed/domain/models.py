from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Document:
    doc_id: str
    text: str
    metadata: Dict[str, str]

@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    metadata: Dict[str, str]

@dataclass(frozen=True)
class SearchHit:
    chunk_id: str
    doc_id: str
    text: str
    score: float
    metadata: Dict[str, str]

@dataclass(frozen=True)
class SearchResponse:
    query: str
    hits: List[SearchHit]
