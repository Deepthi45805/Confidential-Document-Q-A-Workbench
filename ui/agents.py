import streamlit as st

def render_agents():
    st.title("🤖 Multi-Agent Architecture")
    st.markdown("Detailed breakdown of specialized autonomous agents operating within DocShield AI.")

    st.markdown("""
    ### 1. 🧠 Orchestrator Agent
    * **Role**: Primary dispatch and context classifier.
    * **Function**: Evaluates natural language user prompts and determines whether to invoke RAG, Summarization, or Comparative Analysis based on intent heuristics and semantic classification.

    ---

    ### 2. 💬 Q&A Agent (RAG Specialist)
    * **Role**: Grounded document retrieval and query answering.
    * **Function**: Computes text embeddings using `all-MiniLM-L6-v2`, executes vector similarity queries against ChromaDB, and forces non-hallucinatory LLM synthesis.
    * **Safety Constraint**: Explicitly returns *"I couldn't find this information in the uploaded documents"* if similarity score drops below safety threshold.

    ---

    ### 3. 📄 Summarizer Agent
    * **Role**: Structured document synthesis.
    * **Function**: Aggregates document chunks into standard executive sections: Key Points, Important Details, Action Items, Important Dates, and Key Terms.

    ---

    ### 4. 🔄 Comparator Agent
    * **Role**: Multi-version document differential analysis.
    * **Function**: Combines line-level delta computations with LLM synthesis to highlight added, modified, and removed clauses across policy revisions.
    """)
