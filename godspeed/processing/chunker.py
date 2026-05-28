from __future__ import annotations

from typing import Sequence

from godspeed.domain.models import Chunk, Document


class FixedSizeChunkProcessor:
    """Splits documents into fixed-size overlapping chunks."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, documents: Sequence[Document]) -> Sequence[Chunk]:
        chunks = []
        for document in documents:
            text = document.text
            step = self.chunk_size - self.overlap
            for index, start in enumerate(range(0, len(text), step)):
                slice_text = text[start : start + self.chunk_size].strip()
                if not slice_text:
                    continue
                chunks.append(
                    Chunk(
                        chunk_id=f"{document.doc_id}:{index}",
                        doc_id=document.doc_id,
                        text=slice_text,
                        metadata=document.metadata,
                    )
                )
        return chunks

