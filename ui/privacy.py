import streamlit as st
from config.settings import EXECUTION_MODE, OLLAMA_BASE_URL, OLLAMA_MODEL, CHROMA_PERSIST_DIR, SQLITE_DB_PATH

def render_privacy():
    st.title("🔐 Privacy & System Control")
    st.markdown("Zero Cloud Footprint — Enterprise Security Architecture.")

    st.markdown(f"""
    <div style="background-color: #0F172A; padding: 20px; border-radius: 8px; border: 1px solid #38BDF8; margin-bottom: 20px;">
        <h3 style="color: #38BDF8; margin-top: 0;">🛡️ Local Isolation Assurance</h3>
        <ul style="color: #F8FAFC; line-height: 1.8;">
            <li><strong>Execution Mode:</strong> <code>{EXECUTION_MODE}</code></li>
            <li><strong>LLM Provider:</strong> Ollama Local Server (<code>{OLLAMA_BASE_URL}</code>)</li>
            <li><strong>Active Model:</strong> <code>{OLLAMA_MODEL}</code></li>
            <li><strong>Vector Store Path:</strong> <code>{CHROMA_PERSIST_DIR}</code></li>
            <li><strong>Audit Store Path:</strong> <code>{SQLITE_DB_PATH}</code></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Architecture Verification")
    st.markdown("""
    * **No External LLM API Calls**: In `LOCAL` mode, all text generation requests pass exclusively to your loopback adapter (`127.0.0.1:11434`).
    * **Local Embeddings**: Embeddings are computed locally via `sentence-transformers` without sending text to third-party endpoints.
    * **Local Persistence**: Vector indexes and relational audit trails reside entirely on local disk.
    """)
