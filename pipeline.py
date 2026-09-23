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