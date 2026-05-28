from __future__ import annotations

from pathlib import Path
from typing import Sequence

from godspeed.domain.models import Document


class TextDirectoryIngestor:
    """Loads .txt files from a directory into document objects."""

    def ingest(self, source: str) -> Sequence[Document]:
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {source}")

        documents = []
        for path in sorted(source_path.glob("*.txt")):
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            documents.append(
                Document(
                    doc_id=path.stem,
                    text=text,
                    metadata={"source": str(path)},
                )
            )
        return documents

