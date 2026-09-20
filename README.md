# 🛡️ DOCSHIELD AI — Private Multi-Agent Document Intelligence Workbench

> **Capabl Agentic AI Saksham National Level Agentic AI Hackathon**  
> **Problem Statement B1:** Confidential Document Q&A Workbench

---

## 1. Project Overview
**DocShield AI** is an enterprise-grade multi-agent document intelligence platform built to operate **100% locally**. It eliminates sensitive corporate data exposure by keeping documents, embedding generation, vector search, and LLM inference entirely on-premise.

## 2. Problem Statement
Organizations routinely deal with sensitive internal policies, legal contracts, and financial reports. Standard cloud-based AI solutions pose severe data privacy, compliance, and IP leakage risks. **DocShield AI** solves this by establishing a secure, air-gapped agentic workbench over local files.

## 3. Key Features
- 🔐 **Privacy First**: Local AI inference powered by Ollama (`llama3:8b`).
- 🧠 **Agentic Orchestration**: Dynamic request routing via intelligent Orchestrator.
- 💬 **Grounded RAG Q&A**: Hallucination-resistant answers with precise page-level citations.
- 📄 **Executive Summarizer**: Structured breakdowns (Key Points, Dates, Terms, Action Items).
- 🔄 **Document Comparator**: Clause-by-clause differential comparison across file versions.
- 📋 **Local Audit Trail**: SQLite compliance logging tracking timestamps, invoked agents, and accessed files.

## 4. System Architecture
USER
↓
STREAMLIT UI
↓
ORCHESTRATOR AGENT
↓
┌───────────────────────────────┐
│                               │
↓               ↓               ↓
Q&A AGENT    SUMMARIZER     COMPARATOR
│               │               │
↓               ↓               ↓
RETRIEVAL     DOCUMENT        DOCUMENT
RAG           ANALYSIS        COMPARISON
│               │               │
└───────────────┴───────────────┘
↓
FINAL RESPONSE + CITATIONS + LOCAL AUDIT LOG

## 5. Technology Stack
- **Frontend**: Streamlit
- **Agent Orchestration**: LangGraph
- **LLM**: Ollama (`llama3:8b`)
- **Vector DB**: ChromaDB
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Document Parsers**: PyMuPDF (`fitz`), `python-docx`
- **Audit Storage**: SQLite
- **Language**: Python 3.11+

## 6. Installation & Setup

```bash
# Clone the repository
git clone [https://github.com/your-repo/docshield-ai.git](https://github.com/your-repo/docshield-ai.git)
cd docshield-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
