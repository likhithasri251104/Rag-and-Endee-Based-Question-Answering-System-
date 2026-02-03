# RAG-based Document Question Answering System

This project demonstrates a Retrieval Augmented Generation system using **Endee** as the vector database.

## Features
- Semantic search
- RAG pipeline
- Agentic AI logic

## Setup

**1. Start Endee Database (required)**
```bash
docker compose up -d
```
Ensure the Endee container is running on port 8080 before proceeding.

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Ingest Documents**
```bash
python scripts/ingest.py
```

**4. Run the API Server**
```bash
uvicorn backend.app:app --reload
```

Visit `http://localhost:8000/ask?question=What%20is%20a%20vector%20database` to test.

## Troubleshooting

- **Internal Server Error / 503**: Ensure Endee Docker is running (`docker compose up -d`) and documents are ingested (`python scripts/ingest.py`).
- **Connection refused**: The Endee database must be running at `localhost:8080` before the API can respond.
