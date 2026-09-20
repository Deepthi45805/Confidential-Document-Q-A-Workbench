import os
import json
from typing import List, Dict, Any, Optional
from document_processing.parser import DocumentParser
from document_processing.chunker import DocumentChunker
from document_processing.embeddings import EmbeddingManager
from database.chroma_db import ChromaDBManager
from config.settings import DATA_DIR

class DocumentService:
    def __init__(self):
        self.parser = DocumentParser()
        self.chunker = DocumentChunker()
        self.embedding_mgr = EmbeddingManager()
        self.db = ChromaDBManager()
        self.metadata_file = os.path.join(DATA_DIR, "documents_meta.json")
        self.processed_docs = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_metadata(self):
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.processed_docs, f, indent=2)

    def process_and_store_document(self, file_path: str) -> Dict[str, Any]:
        parsed_doc = self.parser.parse_document(file_path)
        doc_id = parsed_doc["file_name"]

        chunks = self.chunker.chunk_document(parsed_doc)
        
        texts = [c["text"] for c in chunks]
        metadatas = [
            {
                "doc_id": c["doc_id"],
                "page_number": c["page_number"],
                "chunk_id": c["chunk_id"]
            }
            for c in chunks
        ]
        ids = [c["chunk_id"] for c in chunks]

        embeddings = self.embedding_mgr.embed_batch(texts)

        # Clean existing if updating
        self.db.delete_document_chunks(doc_id)
        
        # Add to vector store
        self.db.add_chunks(
            chunks=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        doc_meta = {
            "doc_id": doc_id,
            "file_name": doc_id,
            "file_path": file_path,
            "file_type": parsed_doc["file_type"],
            "file_size": parsed_doc["file_size"],
            "total_pages": parsed_doc["total_pages"],
            "total_chunks": len(chunks),
            "full_text": parsed_doc["full_text"]
        }

        self.processed_docs[doc_id] = doc_meta
        self._save_metadata()

        return doc_meta

    def list_documents(self) -> List[Dict[str, Any]]:
        return list(self.processed_docs.values())

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.processed_docs.get(doc_id)

    def delete_document(self, doc_id: str):
        if doc_id in self.processed_docs:
            doc_meta = self.processed_docs[doc_id]
            if os.path.exists(doc_meta["file_path"]):
                try:
                    os.remove(doc_meta["file_path"])
                except Exception:
                    pass
            self.db.delete_document_chunks(doc_id)
            del self.processed_docs[doc_id]
            self._save_metadata()

    def get_context_for_query(self, query: str, n_results: int = 4, doc_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_mgr.embed_text(query)
        results = self.db.query(query_embedding, n_results=n_results, filter_doc_id=doc_id)

        retrieved = []
        if results and results.get("documents") and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                retrieved.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                })
        return retrieved
