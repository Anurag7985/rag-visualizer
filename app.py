from utils.llm import load_llm
from utils.llm import generate_answer
from utils.retriever import search
from utils.vector_store import create_vector_store
from utils.chunker import create_chunks
from utils.embedding import load_embedding_model
from utils.save_file import save_file
import streamlit as st
import os

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

    save_file(file_path, uploaded_file)

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

    #chunk setting
    chunks = st.slider(
        "Chunk Size",
         min_value=100,
          max_value=500,
          value=200,
          step=10
    )

    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=0,
        max_value=100,
        value=20,
        step=10
    )

    chunks = create_chunks(
        documents,
        chunks,
        chunk_overlap)

    with col2:
        st.metric("Chunks", len(chunks))

    with st.expander("📄 First Chunk"):
        st.write(chunks[0].page_content)
    
     # Embedding Model
    embedding_model = load_embedding_model()

    # Create vector store
    vector_store = create_vector_store(chunks, embedding_model)

    st.success("✅ Vector Store Created")

    st.divider()

    query = st.text_input("Ask a question about your PDF")

    results = search(vector_store, query)

    context = ""

    for doc in results:
        context += doc.page_content + "\n\n"

    llm = load_llm()

    llm_response = generate_answer(llm, context, query)

    st.subheader("Answer")

    st.write(llm_response)


    