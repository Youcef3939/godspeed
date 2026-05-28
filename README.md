# Godspeed

Godspeed is a modular AI-native search and retrieval backend designed with cleanly separated layers so each part can be swapped with distributed alternatives as scale grows.

## Architecture

`godspeed/` is intentionally split by responsibilities:

- **ingestion**: raw source loading (`TextDirectoryIngestor`)
- **processing**: chunking and normalization (`FixedSizeChunkProcessor`)
- **embedding**: embedding adapter (`SentenceTransformerEmbedder`)
- **storage**: vector index backend (`FaissVectorStore`)
- **retrieval**: ranking/retrieval orchestration (`Retriever`)
- **pipeline**: end-to-end coordinator (`SearchPipeline`)
- **api**: FastAPI service exposing query endpoints
- **interfaces**: contracts/protocols to support backend replacement (distributed queues, remote embedding services, external vector DBs, etc.)

This structure gives a production-friendly, startup-grade base while keeping today's implementation local and easy to run.

## Current End-to-End Stack

- Embeddings: `sentence-transformers` (`all-MiniLM-L6-v2` by default)
- Vector index: local `FAISS` inner-product index
- API: `FastAPI`

Returned query hits include ranking, score, chunk text, and source citation metadata.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local corpus folder of `.txt` files, for example:

```bash
mkdir -p corpus
echo "Godspeed builds modular retrieval systems." > corpus/doc1.txt
echo "FAISS provides fast local vector search." > corpus/doc2.txt
```

Start the API:

```bash
export GODSPEED_CORPUS_DIR=./corpus
uvicorn godspeed.api.main:app --reload
```

## API

### Health

`GET /health`

### Query

`POST /query`

Request:

```json
{
  "query": "modular retrieval",
  "top_k": 3
}
```

Response:

```json
{
  "query": "modular retrieval",
  "hits": [
    {
      "rank": 1,
      "score": 0.83,
      "chunk_id": "doc1:0",
      "doc_id": "doc1",
      "citation": {
        "source": "corpus/doc1.txt"
      },
      "text": "Godspeed builds modular retrieval systems."
    }
  ]
}
```

## Testing

Run focused tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```
