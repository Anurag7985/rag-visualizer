import os
import streamlit as st

from utils.save_file import save_file
from utils.loader import load_pdf
from utils.chunker import create_chunks
from utils.embedding import load_embedding_model
from utils.vector_store import create_vector_store
from utils.retriever import search
from utils.llm import load_llm, generate_answer


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

    # Save PDF
    os.makedirs("data", exist_ok=True)

    file_path = os.path.join("data", uploaded_file.name)

    save_file(file_path, uploaded_file)

    st.success("✅ PDF uploaded successfully.")

    # Load PDF
    documents = load_pdf(file_path)

    st.subheader("📄 Document Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Pages", len(documents))

    with col2:
        st.metric("File", uploaded_file.name)

    with st.expander("Preview First Page"):
        st.write(documents[0].page_content)

    st.divider()

    # Chunk Settings
    chunk_size = st.slider(
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

    # Create Chunks
    chunks = create_chunks(
        documents,
        chunk_size,
        chunk_overlap
    )

    st.metric("Total Chunks", len(chunks))

    with st.expander("First Chunk"):
        st.write(chunks[0].page_content)

    st.divider()

    # Embedding Model
    embedding_model = load_embedding_model()

    # Vector Store
    vector_store = create_vector_store(
        chunks,
        embedding_model
    )

    st.success("✅ Vector Store Ready")

    st.divider()

    # User Query
    query = st.text_input(
        "Ask a question about your PDF"
    )

    if query.strip():

        with st.spinner("Searching relevant chunks..."):

            results = search(
                vector_store,
                query
            )

        st.subheader("📚 Retrieved Chunks")

        context = ""

        for i, doc in enumerate(results, start=1):

            context += doc.page_content + "\n\n"

            with st.expander(f"Chunk {i}"):
                st.write(doc.page_content)

        with st.spinner("Generating Answer..."):

            llm = load_llm()

            answer = generate_answer(
                llm,
                context,
                query
            )

        st.subheader("🤖 Final Answer")

        st.write(answer)