import streamlit as st

from generation.answer_generator import AnswerGenerator
from indexing.vector_store import VectorStore
from retrieval.vector_retriever import VectorRetriever


st.set_page_config(
    page_title="Advanced RAG",
    page_icon="📚",
    layout="wide",
)


@st.cache_resource
def initialize_rag():

    vector_store = VectorStore()

    retriever = VectorRetriever(
        vector_store=vector_store
    )

    generator = AnswerGenerator()

    return retriever, generator


def main():

    st.title("Advanced RAG")

    retriever, generator = initialize_rag()

    query = st.text_input(
        "Ask a question",
        placeholder="Enter your question...",
    )

    top_k = st.slider(
        "Number of retrieved chunks",
        min_value=1,
        max_value=10,
        value=5,
    )

    if st.button("Search"):

        if not query.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Retrieving relevant information..."):

            results = retriever.retrieve(
                query=query,
                top_k=top_k,
            )

        if not results:
            st.info("No relevant information was found.")
            return

        with st.spinner("Generating answer..."):

            answer = generator.generate(
                query=query,
                results=results,
            )

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Retrieved Sources")

        for index, result in enumerate(results, start=1):

            metadata = result.chunk.metadata

            source = metadata.get(
                "source",
                "Unknown source",
            )

            page = metadata.get("page")

            if page is not None:
                source = f"{source} — page {page}"

            with st.expander(
                f"Source {index}: {source}"
            ):
                st.write(result.chunk.text)


if __name__ == "__main__":
    main()