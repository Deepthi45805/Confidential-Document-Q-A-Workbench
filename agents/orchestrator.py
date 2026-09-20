import json
import time
from typing import Dict, Any, List, Optional
from services.llm_service import LLMService
from services.document_service import DocumentService
from agents.qa_agent import QAAgent
from agents.summarizer_agent import SummarizerAgent
from agents.comparator_agent import ComparatorAgent
from database.audit_log import AuditLogger

class OrchestratorAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.doc_service = DocumentService()
        self.qa_agent = QAAgent(self.llm_service, self.doc_service)
        self.summarizer_agent = SummarizerAgent(self.llm_service, self.doc_service)
        self.comparator_agent = ComparatorAgent(self.llm_service, self.doc_service)
        self.audit_logger = AuditLogger()

    def route_request(self, user_request: str) -> Dict[str, str]:
        req_lower = user_request.lower()

        if any(kw in req_lower for kw in ["summarize", "summary", "overview", "executive summary"]):
            return {
                "agent": "SUMMARIZER",
                "reason": "Request contains explicit summarization keywords asking for high-level document synthesis."
            }
        elif any(kw in req_lower for kw in ["compare", "difference", "versus", "vs", "changed between", "v1 and v2"]):
            return {
                "agent": "COMPARATOR",
                "reason": "Request asks for document comparison and structural delta identification."
            }
        else:
            return {
                "agent": "QA",
                "reason": "Request is a direct factual query requiring vector search and RAG extraction."
            }

    def process(self, user_request: str, target_doc: Optional[str] = None, compare_doc: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Routing decision
        route = self.route_request(user_request)
        selected_agent_type = route["agent"]
        routing_reason = route["reason"]

        result = {}
        docs_accessed = []

        # 2. Execution path
        if selected_agent_type == "SUMMARIZER":
            if not target_doc:
                docs = self.doc_service.list_documents()
                if docs:
                    target_doc = docs[0]["file_name"]
            
            if target_doc:
                docs_accessed.append(target_doc)
                agent_res = self.summarizer_agent.run(target_doc)
                result = {
                    "response_text": agent_res["summary"],
                    "details": agent_res
                }
            else:
                result = {
                    "response_text": "Please upload a document before requesting a summary.",
                    "details": {}
                }

        elif selected_agent_type == "COMPARATOR":
            docs = self.doc_service.list_documents()
            doc1 = target_doc
            doc2 = compare_doc

            if not doc1 and len(docs) > 0:
                doc1 = docs[0]["file_name"]
            if not doc2 and len(docs) > 1:
                doc2 = docs[1]["file_name"]

            if doc1 and doc2:
                docs_accessed.extend([doc1, doc2])
                agent_res = self.comparator_agent.run(doc1, doc2)
                result = {
                    "response_text": agent_res["analysis"],
                    "details": agent_res
                }
            else:
                result = {
                    "response_text": "At least two documents are required in the repository to perform a comparison.",
                    "details": {}
                }

        else:  # QA Agent
            if target_doc:
                docs_accessed.append(target_doc)

            agent_res = self.qa_agent.run(user_request, doc_id=target_doc)
            result = {
                "response_text": agent_res["answer"],
                "details": agent_res
            }

        elapsed_ms = (time.time() - start_time) * 1000

        # 3. Log to Audit
        self.audit_logger.log_event(
            user_request=user_request,
            selected_agent=selected_agent_type,
            routing_reason=routing_reason,
            documents_accessed=docs_accessed,
            status="Completed" if result.get("response_text") else "Failed",
            execution_time_ms=elapsed_ms
        )

        return {
            "request": user_request,
            "orchestrator_decision": {
                "selected_agent": selected_agent_type,
                "reason": routing_reason
            },
            "documents_accessed": docs_accessed,
            "execution_time_ms": elapsed_ms,
            "result": result
        }
