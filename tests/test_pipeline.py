import unittest

from godspeed.domain.models import Document
from godspeed.pipeline import SearchPipeline
from godspeed.processing.chunker import FixedSizeChunkProcessor
from godspeed.storage.faiss_store import FaissVectorStore


class StubIngestor:
    def ingest(self, source: str):
        return [
            Document(doc_id="doc1", text="Cats are great pets.", metadata={"source": "doc1.txt"}),
            Document(doc_id="doc2", text="Dogs love playing fetch.", metadata={"source": "doc2.txt"}),
        ]


class StubKeywordEmbedder:
    def embed(self, texts):
        vectors = []
        for text in texts:
            lowered = text.lower()
            vectors.append(
                [
                    float("cat" in lowered or "cats" in lowered),
                    float("dog" in lowered or "dogs" in lowered),
                ]
            )
        return vectors


class SearchPipelineTests(unittest.TestCase):
    def test_end_to_end_retrieval_returns_ranked_cited_chunks(self):
        pipeline = SearchPipeline(
            ingestor=StubIngestor(),
            processor=FixedSizeChunkProcessor(chunk_size=200, overlap=20),
            embedder=StubKeywordEmbedder(),
            store=FaissVectorStore(),
        )

        indexed_count = pipeline.index("unused")
        response = pipeline.query("cat", top_k=1)

        self.assertEqual(indexed_count, 2)
        self.assertEqual(response.query, "cat")
        self.assertEqual(len(response.hits), 1)
        self.assertEqual(response.hits[0].doc_id, "doc1")
        self.assertEqual(response.hits[0].metadata["source"], "doc1.txt")


if __name__ == "__main__":
    unittest.main()
