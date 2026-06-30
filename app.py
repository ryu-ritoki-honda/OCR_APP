import hashlib

import streamlit as st

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_API_VERSION,
    CHAT_MODEL
)

from utils.azure_embeddings import create_embedding
from utils.models import AppState

from services.document_service import DocumentService
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
from services.answer_service import AnswerService


st.set_page_config(
    page_title="OCR + Semantic Search",
    layout="wide"
)

st.title("OCR + Semantic Search Demo")


# ---------------------------------------------------
# Initialize Services
# ---------------------------------------------------

document_service = DocumentService()
embedding_service = EmbeddingService()
search_service = SearchService()
answer_service = AnswerService(
    endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    deployment=CHAT_MODEL
)


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "state" not in st.session_state:
    st.session_state.state = AppState()

state: AppState = st.session_state.state


# ---------------------------------------------------
# Upload PDF
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    pdf_bytes = uploaded_file.read()

    file_hash = hashlib.md5(pdf_bytes).hexdigest()

    if state.last_file_hash != file_hash:

        with st.spinner("Processing document..."):

            state.result = document_service.process(pdf_bytes)

            state.vector_store = None
            state.embeddings_generated = False
            state.last_file_hash = file_hash

    if state.result is None:
        st.stop()

    result = state.result

    st.success(
        f"{len(result.pages)} page(s) processed."
    )

    # ---------------------------------------------------
    # Combined Document
    # ---------------------------------------------------

    st.subheader("Combined Document")

    st.text_area(
        "Document",
        result.document,
        height=300
    )

    st.download_button(
        "Download Document",
        result.document,
        file_name="document.txt",
        mime="text/plain"
    )

    # ---------------------------------------------------
    # Generate Embeddings
    # ---------------------------------------------------

    if not state.embeddings_generated:

        if st.button("Generate Embeddings"):

            with st.spinner("Generating embeddings..."):

                embedding_service.generate(result.chunks)

                state.vector_store = search_service.build(
                    result.chunks
                )

                state.embeddings_generated = True

            st.success("Embeddings generated.")

    # ---------------------------------------------------
    # Semantic Search + GPT
    # ---------------------------------------------------

    if state.embeddings_generated and state.vector_store is not None:

        question = st.text_input(
            "Ask a question"
        )

        if question:

            with st.spinner("Searching..."):

                question_embedding = create_embedding(question)

                indices, scores = search_service.search(
                    state.vector_store,
                    question_embedding,
                    k=8
                )

            retrieved_chunks = [
                result.chunks[idx]
                for idx in indices
            ]

            st.header("Relevant Chunks")

            for chunk in retrieved_chunks:

                with st.expander(
                    f"Page {chunk.page_number}"
                ):

                    st.write(chunk.text)

            with st.spinner("Generating answer..."):

                answer = answer_service.answer(
                    question,
                    retrieved_chunks
                )

            st.header("Answer")

            st.write(answer)

    # ---------------------------------------------------
    # Page Viewer
    # ---------------------------------------------------

    st.header("Pages")

    for page in result.pages:

        st.divider()

        st.subheader(
            f"Page {page.page_number}"
        )

        tabs = st.tabs([
            "Original",
            "Processed",
            "Digital",
            "OCR",
            "Merged"
        ])

        with tabs[0]:
            st.image(
                page.image,
                use_container_width=True
            )

        with tabs[1]:
            st.image(
                page.processed_image,
                use_container_width=True
            )

        with tabs[2]:
            st.text_area(
                "Digital Text",
                page.digital_text,
                height=450,
                disabled=True,
                key=f"digital_{page.page_number}"
            )

        with tabs[3]:
            st.text_area(
                "OCR Text",
                page.ocr_text,
                height=450,
                disabled=True,
                key=f"ocr_{page.page_number}"
            )

        with tabs[4]:
            st.text_area(
                "Merged Text",
                page.merged_text,
                height=450,
                disabled=True,
                key=f"merged_{page.page_number}"
            )