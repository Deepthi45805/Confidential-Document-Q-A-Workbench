import streamlit as st
from agents.summarizer_agent import SummarizerAgent
from services.llm_service import LLMService
from services.document_service import DocumentService
from database.audit_log import AuditLogger
import time

def render_summarize():
    st.title("📄 Summarizer Agent")
    st.markdown("Extract structured executive summaries, action items, and key terms.")

    doc_service = DocumentService()
    docs = doc_service.list_documents()

    if not docs:
        st.warning("No documents available. Please upload a file in the Documents section first.")
        return

    doc_names = [d["file_name"] for d in docs]
    selected_doc = st.selectbox("Select document to summarize:", doc_names)

    if st.button("Generate Summary", type="primary"):
        llm = LLMService()
        agent = SummarizerAgent(llm, doc_service)
        audit = AuditLogger()

        start = time.time()
        with st.spinner(f"Analyzing and summarizing '{selected_doc}'..."):
            res = agent.run(selected_doc)
            elapsed = (time.time() - start) * 1000

            st.markdown(res["summary"])

            audit.log_event(
                user_request=f"Summarize document {selected_doc}",
                selected_agent="SUMMARIZER",
                routing_reason="Direct invocation of Summarizer UI page.",
                documents_accessed=[selected_doc],
                status="Completed",
                execution_time_ms=elapsed
            )
