import json
from pathlib import Path

import chromadb


from app.models.models import Chunk
from app.vector_store.vectorStore import VectorStore
from sentence_transformers import SentenceTransformer
from app.embeddings.embedder import Embedder
from typing import Any
import numpy as np



class ChromaStore(VectorStore):
    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(self, sections: list[Chunk]):
        ids, texts, metadatas = self.to_chroma_format(sections)
        embeddings = self.embedder.embed(texts)

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,

            
            metadatas=metadatas
        )

    def to_chroma_format(self, chunks):
        ids, texts, metadatas = [], [], []

        for c in chunks:
            meta = {
                "source_file": str(c.source_file),
                "document_type": str(c.document_type),
                "chunk_index": int(c.chunk_index) if c.chunk_index is not None else None,
                "page": c.page,
                "section": str(c.section) if c.section else None,
                "sheet": str(c.sheet) if c.sheet else None,
            }

            # merge extra metadata but flatten values
            for k, v in (c.metadata or {}).items():
                meta[k] = self.sanitize_metadata(v)

            # FINAL safety check
            meta = {k: v for k, v in meta.items() if isinstance(v, (str, int, float, bool))}



            ids.append(c.id)
            texts.append(c.text)
            metadatas.append(meta)
        
        for i, m in enumerate(metadatas):
            for k, v in m.items():
                if not isinstance(v, (str, int, float, bool)):
                    print(f"[BAD METADATA] chunk={i} key={k!r} type={type(v).__name__} value={v!r}")

        return ids, texts, metadatas
    

    def sanitize_metadata(self, value: Any) -> Any:
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, bool):   # bool before int — bool is a subclass of int
            return value
        if isinstance(value, (str, int, float)):
            return value
        if value is None:
            return None               # caller will drop this key
        if isinstance(value, dict):
            return {
                k: sanitized
                for k, v in value.items()
                if (sanitized := self.sanitize_metadata(v)) is not None
            }
        if isinstance(value, list):
            return json.dumps(value, ensure_ascii=False)
        return str(value)
    

    def query(self, query: str, top_k: int = 5) -> list[Chunk]:
        query_embedding = self.embedder.embed([query])

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        return results
