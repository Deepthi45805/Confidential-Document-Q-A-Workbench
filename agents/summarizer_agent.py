from typing import Dict, Any
from services.llm_service import LLMService
from services.document_service import DocumentService

class SummarizerAgent:
    def __init__(self, llm_service: LLMService, doc_service: DocumentService):
        self.llm_service = llm_service
        self.doc_service = doc_service

    def run(self, doc_id: str) -> Dict[str, Any]:
        doc = self.doc_service.get_document(doc_id)
        if not doc:
            return {
                "agent_name": "Summarizer Agent",
                "summary": f"Document '{doc_id}' not found in local repository.",
                "doc_id": doc_id,
                "status": "Failed"
            }

        full_text = doc["full_text"]
        
        # Truncate text if excessively large for local LLM window
        max_chars = 12000
        truncated_text = full_text[:max_chars]

        system_prompt = "You are an executive document summarizer. Generate structured summaries with specific section headers."

        prompt = f"""Please summarize the following document: '{doc_id}'

DOCUMENT CONTENT:
{truncated_text}

OUTPUT STRUCTURE REQUIRED:
### Executive Summary
[Brief high-level overview]

### Key Points
[Bullet points of primary takeaways]

### Important Details
[Specific rules, provisions, or standards]

### Action Items
[Clear tasks or requirements mentioned]

### Important Dates
[Mentioned deadlines or effective dates]

### Key Terms
[Definitions or critical jargon]
"""

        summary_output = self.llm_service.generate(prompt, system_prompt=system_prompt)

        return {
            "agent_name": "Summarizer Agent",
            "doc_id": doc_id,
            "summary": summary_output,
            "status": "Completed",
            "pages_processed": doc["total_pages"]
        }
