import os
import streamlit as st

from utils.loader import load_pdf

st.set_page_config(
    page_title="RAG Visualizer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Visualizer")
st.write("Understand how Retrieval-Augmented Generation (RAG) works step by step.")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs("data", exist_ok=True)

    file_path = os.path.join("data", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ PDF uploaded successfully.")

    documents = load_pdf(file_path)

    st.subheader("Document Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Pages", len(documents))

    with col2:
        st.metric("File Name", uploaded_file.name)

    with st.expander("Preview First Page"):
        st.write(documents[0].page_content)