import streamlit as st
from ui.dashboard import render_dashboard
from ui.documents import render_documents
from ui.ask_ai import render_ask_ai
from ui.summarize import render_summarize
from ui.compare import render_compare
from ui.agents import render_agents
from ui.audit import render_audit
from ui.privacy import render_privacy

st.set_page_config(
    page_title="DocShield AI — Private Multi-Agent Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Custom Styling Injection
st.markdown("""
<style>
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
    }
    .stSidebar {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.sidebar.title("🛡️ DOCSHIELD AI")
    st.sidebar.caption("Private Multi-Agent Workbench")

    if "nav" not in st.session_state:
        st.session_state["nav"] = "Dashboard"

    nav_options = [
        "Dashboard",
        "Documents",
        "Ask AI",
        "Summarize",
        "Compare",
        "Agent Activity",
        "Audit Log",
        "System / Privacy"
    ]

    selected_nav = st.sidebar.radio("Navigation", nav_options, index=nav_options.index(st.session_state["nav"]))
    st.session_state["nav"] = selected_nav

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Privacy Guarantee:**
    🔐 100% Local Processing
    💻 Zero External API Calls
    """)

    if selected_nav == "Dashboard":
        render_dashboard()
    elif selected_nav == "Documents":
        render_documents()
    elif selected_nav == "Ask AI":
        render_ask_ai()
    elif selected_nav == "Summarize":
        render_summarize()
    elif selected_nav == "Compare":
        render_compare()
    elif selected_nav == "Agent Activity":
        render_agents()
    elif selected_nav == "Audit Log":
        render_audit()
    elif selected_nav == "System / Privacy":
        render_privacy()

if __name__ == "__main__":
    main()
