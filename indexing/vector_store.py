from dataclasses import dataclass
from ingestion.document import Chunk
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

@dataclass
class SearchResult:
    chunk: Chunk
    score: float

class VectorStore():
    def __init__(
        self, 
        persist_directory: str= "data/chroma",
        collection_name: str= "documents", 
        embedding_model: str= "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.persist_directory = Path(persist_directory)
        self.client = chromadb.PersistentClient(path = str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(name= collection_name)
        self.embedding_model = SentenceTransformer(embedding_model)


    def add(self, chunks: list[Chunk] ) -> None:
        if not chunks: 
            return

        texts = [chunk.text for chunk in chunks]
        chunks_ids = [chunk.metadata["chunk_id"] for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        self.collection.upsert(
            ids=chunks_ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        self.collection.delete(
            where={"document_id": document_id}
        )

    def re_index_document(
        self,
        document_id: str,
        chunks: list[Chunk]
    ):
        self.delete_document(document_id)
        self.add(chunks)

    def similarity_search(
        self, 
        query: str,
        k: int = 5,
        filters: dict | None = None
    ) -> list[SearchResult]:
        
        if not query.strip():
            return []

        embedded_query = self.embedding_model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        results = self.collection.query(
            query_embeddings=[embedded_query.tolist()],
            n_results= k,
            where= filters
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        search_results = []

        for document, metadata, distance in zip(documents, metadatas, distances):
            temp_chunk = Chunk(
                text = document,
                metadata=metadata
            )

            search_results.append(
                SearchResult(
                    chunk= temp_chunk,
                    score = distance
                )
            )

        return search_results

    def count(self) -> int:
        return self.collection.count()
