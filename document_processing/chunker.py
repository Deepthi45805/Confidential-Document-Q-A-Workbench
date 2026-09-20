from typing import List, Dict, Any
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentChunker:
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        chunks = []
        chunk_id_counter = 0
        file_name = parsed_doc["file_name"]

        for page in parsed_doc["pages"]:
            page_num = page["page_number"]
            text = page["text"]
            
            if not text.strip():
                continue

            words = text.split()
            if not words:
                continue

            # Character or word based sliding window
            # Here using word-based chunking for structural stability
            words_per_chunk = max(20, self.chunk_size // 5)  # Avg 5 chars per word
            overlap_words = max(5, self.chunk_overlap // 5)
            
            i = 0
            while i < len(words):
                chunk_words = words[i:i + words_per_chunk]
                chunk_text = " ".join(chunk_words)
                
                chunks.append({
                    "chunk_id": f"{file_name}_p{page_num}_c{chunk_id_counter}",
                    "doc_id": file_name,
                    "page_number": page_num,
                    "text": chunk_text,
                    "char_count": len(chunk_text)
                })
                
                chunk_id_counter += 1
                i += (words_per_chunk - overlap_words)
                if i <= 0:
                    break

        return chunks
