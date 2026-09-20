import difflib
from typing import Dict, Any, List
from services.llm_service import LLMService
from services.document_service import DocumentService

class ComparatorAgent:
    def __init__(self, llm_service: LLMService, doc_service: DocumentService):
        self.llm_service = llm_service
        self.doc_service = doc_service

    def run(self, doc_id_v1: str, doc_id_v2: str) -> Dict[str, Any]:
        doc1 = self.doc_service.get_document(doc_id_v1)
        doc2 = self.doc_service.get_document(doc_id_v2)

        if not doc1 or not doc2:
            return {
                "agent_name": "Comparator Agent",
                "status": "Failed",
                "error": "One or both selected documents could not be found."
            }

        text1 = doc1["full_text"]
        text2 = doc2["full_text"]

        # Synthesize textual diff analysis
        lines1 = [line.strip() for line in text1.splitlines() if line.strip()]
        lines2 = [line.strip() for line in text2.splitlines() if line.strip()]

        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))

        added = [line[2:] for line in diff if line.startswith('+ ')]
        removed = [line[2:] for line in diff if line.startswith('- ')]

        # Ask LLM to synthesize human-readable delta
        prompt = f"""Compare the following two documents and identify meaningful policy, legal, or procedural changes.

DOCUMENT 1 ({doc_id_v1}):
{text1[:4000]}

DOCUMENT 2 ({doc_id_v2}):
{text2[:4000]}

STRUCTURE YOUR RESPONSE AS:
### Key Changes Overview
[Provide a clear narrative summary of major changes]

### Critical Modifications
- **V1:** [Original text/rule]
  **V2:** [Updated text/rule]
  **Impact:** [Explanation of what changed]

### Added Provisions
[Bullet points of new requirements]

### Removed Provisions
[Bullet points of deprecated requirements]
"""

        llm_analysis = self.llm_service.generate(prompt)

        return {
            "agent_name": "Comparator Agent",
            "doc_v1": doc_id_v1,
            "doc_v2": doc_id_v2,
            "added_count": len(added),
            "removed_count": len(removed),
            "added_samples": added[:5],
            "removed_samples": removed[:5],
            "analysis": llm_analysis,
            "status": "Completed"
        }
