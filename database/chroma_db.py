import os
import chromadb
from chromadb.config import Settings
from config.settings import CHROMA_PERSIST_DIR, COLLECTION_NAME

class ChromaDBManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PERSIST_DIR),
            settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks, embeddings, metadatas, ids):
        if not chunks:
            return
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_embedding, n_results=4, filter_doc_id=None):
        where_clause = None
        if filter_doc_id:
            where_clause = {"doc_id": filter_doc_id}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_clause
        )
        return results

    def delete_document_chunks(self, doc_id):
        self.collection.delete(where={"doc_id": doc_id})

    def reset_database(self):
        self.client.reset()
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def get_count(self):
        return self.collection.count()
