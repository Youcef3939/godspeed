# GODSPEED

Godspeed is an AI-native search engine that transforms the web into structured, real-time, citation-backed knowledge for humans and AI agents

---

## why?

traditional search engines give you documents to read

AI systems need something different:
- structured knowledge
- verifiable sources
- fast retrieval
- reasoning-ready outputs

---

## what it does

given a query, Godspeed:

- retrieves relevant information from local or external sources
- breaks content into meaningful semantic chunks
- ranks results by relevance
- attaches source citations
- returns structured, machine-readable answers

it is designed to power:
- AI agents
- research systems
- intelligent assistants
- RAG pipelines

---

## architecture

`godspeed/` is split by responsibility to support both local execution and future distributed scaling: 

- **ingestion**: loads raw content (`TextDirectoryIngestor`)
- **processing**: cleaning + chunking (`FixedSizeChunkProcessor`)
- **embedding**: embedding interface (`SentenceTransformerEmbedder`)
- **storage**: vector index layer (`FaissVectorStore`)
- **retrieval**: ranking + search logic (`Retriever`)
- **pipeline**: end-to-end orchestration (`SearchPipeline`)
- **api**: fastAPI service exposing query endpoints
- **interfaces**: abstract contracts for swapping components with distributed systems (vector DBs, remote embedding services, queues, etc..)

---

## diagram

```mermaid
flowchart TD

subgraph group_runtime["Runtime"]
  node_api_main["API<br/>[main.py]"]
  node_query(("Query<br/>Request"))
  node_ranked_results["Results<br/>Response payload"]
end

subgraph group_pipeline["Pipeline"]
  node_pipeline_main["Pipeline<br/>Orchestrator<br/>[pipeline.py]"]
  node_text_ingestor["Ingestor<br/>Text loader<br/>[text_ingestor.py]"]
  node_chunker["Chunker<br/>Text processor<br/>[chunker.py]"]
  node_embedder["Embedder<br/>SentenceTransformer"]
  node_faiss_store[("Vector store<br/>FAISS index<br/>[faiss_store.py]")]
  node_retriever["Retriever<br/>Similarity search<br/>[retriever.py]"]
  node_corpus["Local corpus<br/>Text files"]
  node_indexed_chunks["Chunks<br/>Indexed units"]
end

subgraph group_abstractions["Abstractions"]
  node_models["Models<br/>Domain schema<br/>[models.py]"]
  node_contracts["Contracts<br/>Interfaces<br/>[contracts.py]"]
end

subgraph group_support["Support"]
  node_logging["Logging<br/>Core infra<br/>[logging.py]"]
  node_tests["Tests<br/>Integration test<br/>[test_pipeline.py]"]
end

node_corpus -->|"load"| node_text_ingestor
node_text_ingestor -->|"normalize"| node_chunker
node_chunker -->|"produce"| node_indexed_chunks
node_indexed_chunks -->|"encode"| node_embedder
node_embedder -->|"index"| node_faiss_store
node_api_main -->|"delegate"| node_pipeline_main
node_pipeline_main -->|"query"| node_retriever
node_query -->|"submit"| node_api_main
node_retriever -->|"embed query"| node_embedder
node_retriever -->|"search"| node_faiss_store
node_retriever -->|"shape hits"| node_models
node_pipeline_main -->|"use"| node_models
node_pipeline_main -->|"depend on"| node_contracts
node_api_main -->|"serialize"| node_models
node_logging -.->|"trace"| node_pipeline_main
node_tests -.->|"verify"| node_pipeline_main
node_tests -.->|"verify"| node_api_main

click node_api_main "https://github.com/youcef3939/godspeed/blob/main/godspeed/api/main.py"
click node_pipeline_main "https://github.com/youcef3939/godspeed/blob/main/godspeed/pipeline.py"
click node_text_ingestor "https://github.com/youcef3939/godspeed/blob/main/godspeed/ingestion/text_ingestor.py"
click node_chunker "https://github.com/youcef3939/godspeed/blob/main/godspeed/processing/chunker.py"
click node_embedder "https://github.com/youcef3939/godspeed/blob/main/godspeed/embedding/sentence_transformer.py"
click node_faiss_store "https://github.com/youcef3939/godspeed/blob/main/godspeed/storage/faiss_store.py"
click node_retriever "https://github.com/youcef3939/godspeed/blob/main/godspeed/retrieval/retriever.py"
click node_models "https://github.com/youcef3939/godspeed/blob/main/godspeed/domain/models.py"
click node_contracts "https://github.com/youcef3939/godspeed/blob/main/godspeed/interfaces/contracts.py"
click node_logging "https://github.com/youcef3939/godspeed/blob/main/godspeed/core/logging.py"
click node_tests "https://github.com/youcef3939/godspeed/blob/main/tests/test_pipeline.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_api_main,node_query,node_ranked_results toneBlue
class node_pipeline_main,node_text_ingestor,node_chunker,node_embedder,node_faiss_store,node_retriever,node_corpus,node_indexed_chunks toneAmber
class node_models,node_contracts toneMint
class node_logging,node_tests toneRose
```

---

## current implementation

- embeddings: `sentence-transformers` (`all-MiniLM-L6-v2`)
- vector search: local `FAISS`
- API layer: `fastAPI`
- input source: local text corpus (`.txt` files)

---

## quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

create a corpus
```
mkdir -p corpus
echo "Godspeed builds AI-native retrieval systems." > corpus/doc1.txt
echo "FAISS enables fast vector similarity search." > corpus/doc2.txt
```

run 
```
export GODSPEED_CORPUS_DIR=./corpus
uvicorn godspeed.api.main:app --reload
```

---

## API
### health check
`GET /health`

### query
`POST /query`

```
{
  "query": "vector search systems",
  "top_k": 3
}
```

response:
```
{
  "query": "vector search systems",
  "hits": [
    {
      "rank": 1,
      "score": 0.83,
      "chunk_id": "doc1:0",
      "doc_id": "doc1",
      "citation": {
        "source": "corpus/doc1.txt"
      },
      "text": "Godspeed builds AI-native retrieval systems."
    }
  ]
}
```
