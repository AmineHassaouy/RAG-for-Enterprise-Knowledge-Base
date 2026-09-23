from ingestion.base_loader import BaseLoader
from processing.chunking import Chunker
from processing.metadata import MetadataProcessor
from indexing.vector_store import VectorStore


class RAGPipeline:

    def __init__(
        self,
        metadata_processor: MetadataProcessor,
        vector_store: VectorStore,
    ):
        self.metadata_processor = metadata_processor
        self.vector_store = vector_store

    def ingest(
        self,
        loader: BaseLoader,
        source,
        chunker: Chunker,
    ) -> None:

        documents = loader.load(source)

        if isinstance(documents, list):
            loaded_documents = documents
        else:
            loaded_documents = [documents]

        for document in loaded_documents:

            document = self.metadata_processor.process_document(
                document
            )

            chunks = chunker.chunk(document)

            chunks = self.metadata_processor.process_chunks(
                chunks
            )

            self.vector_store.reindex(
                document_id=document.metadata["document_id"],
                chunks=chunks,
            )