from typing import Dict, Any, List
from services.llm_service import LLMService
from services.document_service import DocumentService

class QAAgent:
    def __init__(self, llm_service: LLMService, doc_service: DocumentService):
        self.llm_service = llm_service
        self.doc_service = doc_service

    def run(self, query: str, doc_id: str = None) -> Dict[str, Any]:
        retrieved_chunks = self.doc_service.get_context_for_query(query, n_results=4, doc_id=doc_id)

        if not retrieved_chunks:
            return {
                "agent_name": "Q&A Agent",
                "answer": "I couldn't find this information in the uploaded documents because no relevant documents or text chunks match your request.",
                "sources": [],
                "grounded": False,
                "confidence": 0.0
            }

        context_str = ""
        sources = []
        for i, chunk in enumerate(retrieved_chunks):
            context_str += f"\n--- Document Chunk {i+1} (Source: {chunk['metadata']['doc_id']}, Page {chunk['metadata']['page_number']}) ---\n"
            context_str += chunk['text'] + "\n"
            
            sources.append({
                "doc_id": chunk['metadata']['doc_id'],
                "page_number": chunk['metadata']['page_number'],
                "snippet": chunk['text'][:150] + "...",
                "distance": float(chunk.get("distance", 0.0))
            })

        system_prompt = """You are a strictly grounded document Q&A assistant. 
Answer the user query based ONLY on the provided document contexts below. 
If the answer cannot be directly determined from the provided context, state explicitly: "I couldn't find this information in the uploaded documents."
Do not invent or extrapolate details not present in the context."""

        prompt = f"""DOCUMENT CONTEXT:
{context_str}

USER QUESTION: {query}

Provide a comprehensive, accurate answer grounded solely in the above context."""

        llm_response = self.llm_service.generate(prompt, system_prompt=system_prompt)

        # Check for ungrounded condition or fallback in text
        grounded = "I couldn't find this information" not in llm_response

        return {
            "agent_name": "Q&A Agent",
            "answer": llm_response,
            "sources": sources,
            "grounded": grounded,
            "confidence": 0.92 if grounded else 0.10
        }
