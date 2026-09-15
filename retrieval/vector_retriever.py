from indexing.vector_store import SearchResult, VectorStore

class VectorRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int =5, filters:dict|None = None) -> list[SearchResult]:

        if not query.strip():
            return []

        if top_k <= 0:
            return []

        return self.vector_store.similarity_search(
            query=query,
            k=top_k,
            filters= filters
        )