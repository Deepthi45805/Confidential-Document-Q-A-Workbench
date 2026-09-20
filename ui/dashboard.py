import streamlit as st
from services.document_service import DocumentService
from database.audit_log import AuditLogger
from config.settings import EXECUTION_MODE

def render_dashboard():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 24px; border-radius: 12px; margin-bottom: 24px; border: 1px solid #334155;">
            <h1 style="color: #F8FAFC; margin: 0; font-size: 2.2rem; font-weight: 700;">DOCSHIELD AI</h1>
            <p style="color: #38BDF8; margin-top: 4px; font-size: 1.1rem; font-weight: 500;">Private Multi-Agent Document Intelligence</p>
            <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">“Your documents stay private. Your AI works locally.”</p>
        </div>
    """, unsafe_allow_html=True)

    doc_service = DocumentService()
    audit_logger = AuditLogger()

    docs = doc_service.list_documents()
    logs = audit_logger.get_all_logs(limit=50)

    # Top Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Uploaded Documents", len(docs))
    with m2:
        st.metric("Total Executions", len(logs))
    with m3:
        st.metric("Active Specialists", "3 Agents")
    with m4:
        mode_badge = "🟢 LOCAL AI" if EXECUTION_MODE == "LOCAL" else "🟡 DEMO MODE"
        st.metric("Privacy Status", mode_badge)

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📁 Recent Documents")
        if docs:
            for doc in docs[-5:]:
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #1E293B; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #38BDF8; margin-bottom: 8px;">
                        <strong style="color: #F8FAFC;">{doc['file_name']}</strong> 
                        <span style="color: #94A3B8; font-size: 0.85rem;">({doc['file_type']} | {doc['total_pages']} pages | {doc['total_chunks']} chunks)</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No documents uploaded yet. Go to the Documents tab to upload sample files.")

        st.subheader("⚡ Quick Actions")
        qa1, qa2, qa3 = st.columns(3)
        if qa1.button("💬 Ask Question", use_container_width=True):
            st.session_state["nav"] = "Ask AI"
            st.rerun()
        if qa2.button("📄 Summarize Doc", use_container_width=True):
            st.session_state["nav"] = "Summarize"
            st.rerun()
        if qa3.button("🔄 Compare Versions", use_container_width=True):
            st.session_state["nav"] = "Compare"
            st.rerun()

    with col_right:
        st.subheader("📋 Recent Audit Trail")
        if logs:
            for log in logs[:5]:
                st.markdown(f"""
                <div style="background-color: #0F172A; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #334155; font-size: 0.85rem;">
                    <div style="color: #38BDF8; font-weight: 600;">{log['selected_agent']}</div>
                    <div style="color: #E2E8F0; margin: 2px 0;">{log['user_request'][:40]}...</div>
                    <div style="color: #64748B; font-size: 0.75rem;">{log['timestamp']} | {log['execution_time_ms']:.1f}ms</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.text("No log entries recorded.")
