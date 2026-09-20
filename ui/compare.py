import streamlit as st
from agents.comparator_agent import ComparatorAgent
from services.llm_service import LLMService
from services.document_service import DocumentService
from database.audit_log import AuditLogger
import time

def render_compare():
    st.title("🔄 Comparator Agent")
    st.markdown("Perform side-by-side structural diff and semantic analysis between two document versions.")

    doc_service = DocumentService()
    docs = doc_service.list_documents()

    if len(docs) < 2:
        st.warning("Comparison requires at least two documents in the repository. Please upload additional files or generate sample documents.")
        return

    doc_names = [d["file_name"] for d in docs]
    
    col1, col2 = st.columns(2)
    with col1:
        doc_v1 = st.selectbox("Select Original Document (V1):", doc_names, index=0)
    with col2:
        doc_v2 = st.selectbox("Select Modified Document (V2):", doc_names, index=1 if len(doc_names) > 1 else 0)

    if st.button("Compare Documents", type="primary"):
        if doc_v1 == doc_v2:
            st.error("Please select two different documents for comparison.")
            return

        llm = LLMService()
        agent = ComparatorAgent(llm, doc_service)
        audit = AuditLogger()

        start = time.time()
        with st.spinner(f"Comparing '{doc_v1}' and '{doc_v2}'..."):
            res = agent.run(doc_v1, doc_v2)
            elapsed = (time.time() - start) * 1000

            st.markdown(res["analysis"])

            audit.log_event(
                user_request=f"Compare {doc_v1} vs {doc_v2}",
                selected_agent="COMPARATOR",
                routing_reason="Direct invocation of Comparator UI page.",
                documents_accessed=[doc_v1, doc_v2],
                status="Completed",
                execution_time_ms=elapsed
            )
