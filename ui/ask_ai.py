import streamlit as st
from agents.orchestrator import OrchestratorAgent
from services.document_service import DocumentService

def render_ask_ai():
    st.title("💬 Ask AI — Multi-Agent Intelligence")
    st.markdown("Ask any question. The Orchestrator Agent will analyze your prompt and dispatch the ideal specialist.")

    orchestrator = OrchestratorAgent()
    doc_service = DocumentService()

    docs = doc_service.list_documents()
    doc_options = ["All Documents"] + [d["file_name"] for d in docs]
    
    selected_doc_option = st.selectbox("Scope search to specific document (Optional):", doc_options)
    target_doc = None if selected_doc_option == "All Documents" else selected_doc_option

    # Pre-defined hackathon queries
    st.markdown("**Sample Demo Queries:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    
    query_input = st.text_input("Enter your request:", placeholder="e.g., What is the leave policy?")

    if q_col1.button("What is the leave policy?"):
        query_input = "What is the leave policy?"
    if q_col2.button("Summarize the employee policy"):
        query_input = "Summarize the employee policy"
    if q_col3.button("What changed between Policy V1 and Policy V2?"):
        query_input = "What changed between Policy V1 and Policy V2?"

    if st.button("Submit Request", type="primary") and query_input:
        with st.spinner("Orchestrator routing and executing..."):
            response = orchestrator.process(query_input, target_doc=target_doc)

            dec = response["orchestrator_decision"]
            res_data = response["result"]

            # Workflow Visualization Card
            st.markdown(f"""
            <div style="background-color: #0F172A; padding: 16px; border-radius: 8px; border: 1px solid #38BDF8; margin: 16px 0;">
                <h4 style="color: #38BDF8; margin-top: 0;">🧠 Agentic Workflow Execution</h4>
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.9rem; color: #F8FAFC;">
                    <div><strong>USER REQUEST</strong><br/><span style="color:#94A3B8;">"{query_input}"</span></div>
                    <div>➡️</div>
                    <div><strong>ORCHESTRATOR</strong><br/><span style="color:#38BDF8;">Routing Engine</span></div>
                    <div>➡️</div>
                    <div><strong>SELECTED SPECIALIST</strong><br/><span style="color:#4ADE80; font-size:1.05rem;">{dec['selected_agent']} AGENT</span></div>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #334155; font-size: 0.85rem; color: #CBD5E1;">
                    <strong>Routing Reason:</strong> {dec['reason']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Response Output
            st.subheader("Response")
            st.markdown(res_data.get("response_text", "No response generated."))

            # RAG Citations
            if "details" in res_data and "sources" in res_data["details"] and res_data["details"]["sources"]:
                st.subheader("📚 Grounded Source Citations")
                for src in res_data["details"]["sources"]:
                    with st.expander(f"Source: {src['doc_id']} (Page {src['page_number']})"):
                        st.text(src["snippet"])
