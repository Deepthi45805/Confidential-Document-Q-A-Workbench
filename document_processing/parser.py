import os
import fitz  # PyMuPDF
from docx import Document as DocxDocument
from typing import Dict, Any, List

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        doc = fitz.open(file_path)
        pages_content = []
        full_text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            pages_content.append({
                "page_number": page_num + 1,
                "text": text
            })
            full_text += f"\n--- Page {page_num + 1} ---\n" + text
            
        doc.close()
        return {
            "file_name": os.path.basename(file_path),
            "file_type": "PDF",
            "file_size": os.path.getsize(file_path),
            "total_pages": len(pages_content),
            "full_text": full_text,
            "pages": pages_content
        }

    @staticmethod
    def parse_docx(file_path: str) -> Dict[str, Any]:
        doc = DocxDocument(file_path)
        full_text = ""
        pages_content = []
        
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(paragraphs)
        
        # Approximate pages for DOCX (approx 300 words per page)
        words = full_text.split()
        total_words = len(words)
        approx_pages = max(1, (total_words // 300) + (1 if total_words % 300 > 0 else 0))
        
        # Group paragraphs into synthetic page structures
        words_per_page = 300
        current_page = 1
        current_words = 0
        page_text = ""
        
        for p in paragraphs:
            p_words = len(p.split())
            if current_words + p_words > words_per_page and page_text:
                pages_content.append({
                    "page_number": current_page,
                    "text": page_text
                })
                current_page += 1
                page_text = p + "\n"
                current_words = p_words
            else:
                page_text += p + "\n"
                current_words += p_words
                
        if page_text:
            pages_content.append({
                "page_number": current_page,
                "text": page_text
            })

        return {
            "file_name": os.path.basename(file_path),
            "file_type": "DOCX",
            "file_size": os.path.getsize(file_path),
            "total_pages": len(pages_content) if pages_content else 1,
            "full_text": full_text,
            "pages": pages_content if pages_content else [{"page_number": 1, "text": full_text}]
        }

    @classmethod
    def parse_document(cls, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return cls.parse_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return cls.parse_docx(file_path)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {
                "file_name": os.path.basename(file_path),
                "file_type": "TXT",
                "file_size": os.path.getsize(file_path),
                "total_pages": 1,
                "full_text": content,
                "pages": [{"page_number": 1, "text": content}]
            }
        else:
            raise ValueError(f"Unsupported file format: {ext}")
