import os
import streamlit as st
from services.document_service import DocumentService
from config.settings import DATA_DIR

def render_documents():
    st.title("📁 Document Management")
    st.markdown("Upload, index, and manage confidential files for local RAG processing.")

    doc_service = DocumentService()

    uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx", "txt"])

    if uploaded_file:
        file_path = os.path.join(DATA_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner(f"Indexing '{uploaded_file.name}' into vector database..."):
            meta = doc_service.process_and_store_document(file_path)
            st.success(f"Successfully processed {meta['file_name']} into {meta['total_chunks']} searchable chunks!")

    st.markdown("---")
    st.subheader("Repository Contents")

    docs = doc_service.list_documents()

    if docs:
        for doc in docs:
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.markdown(f"**{doc['file_name']}**")
            c2.text(f"{doc['file_type']} | {doc['total_pages']} pg")
            c3.text(f"{doc['total_chunks']} chunks")
            if c4.button("Delete", key=f"del_{doc['doc_id']}"):
                doc_service.delete_document(doc['doc_id'])
                st.rerun()
    else:
        st.info("Repository is currently empty. Upload files or run the sample document generator.")
