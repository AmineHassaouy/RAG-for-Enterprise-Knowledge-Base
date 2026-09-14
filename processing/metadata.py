from hashlib import sha256
from typing import Iterable

from ingestion.document import Document, Chunk


class MetadataProcessor:

    COMMON_FIELDS = {
        "source",
        "type",
        "title",
        "page",
        "row",
        "document_id",
        "chunk_id",
        "chunk_index",
        "section",
    }

    def process_document(self, document: Document) -> Document:
        metadata = self._normalize_metadata(document.metadata)

        if "document_id" not in metadata:
            metadata["document_id"] = self._generate_document_id(
                document,
                metadata
            )

        return Document(
            text=document.text,
            metadata=metadata
        )

    def process_documents(
        self,
        documents: Iterable[Document]
    ) -> list[Document]:

        return [
            self.process_document(document)
            for document in documents
        ]

    def process_chunks(
        self,
        chunks: Iterable[Chunk]
    ) -> list[Chunk]:

        processed_chunks = []

        for index, chunk in enumerate(chunks):
            metadata = self._normalize_metadata(chunk.metadata)
            metadata = self._remove_processing_metadata(metadata)

            document_id = metadata.get("document_id")

            if not document_id:
                document_id = self._generate_chunk_document_id(
                    chunk,
                    metadata
                )
                metadata["document_id"] = document_id

            metadata["chunk_index"] = index

            metadata["chunk_id"] = self._generate_chunk_id(
                document_id=document_id,
                chunk_index=index,
                text=chunk.text
            )

            processed_chunks.append(
                Chunk(
                    text=chunk.text,
                    metadata=metadata
                )
            )

        return processed_chunks

    def _normalize_metadata(self, metadata: dict) -> dict:
        normalized = {}

        for key, value in metadata.items():
            if value is None:
                continue

            if isinstance(value, str):
                value = value.strip()

            normalized[key] = value

        return normalized

    def _generate_document_id(
        self,
        document: Document,
        metadata: dict
    ) -> str:

        source = metadata.get("source", "")
        document_type = metadata.get("type", "")

        identity = f"{document_type}:{source}"

        return sha256(
            identity.encode("utf-8")
        ).hexdigest()

    def _generate_chunk_document_id(
        self,
        chunk: Chunk,
        metadata: dict
    ) -> str:

        source = metadata.get("source", "")
        document_type = metadata.get("type", "")

        identity = (
            f"{document_type}:"
            f"{source}:"
            f"{chunk.text}"
        )

        return sha256(
            identity.encode("utf-8")
        ).hexdigest()

    def _generate_chunk_id(
        self,
        document_id: str,
        chunk_index: int,
        text: str
    ) -> str:

        identity = (
            f"{document_id}:"
            f"{chunk_index}:"
            f"{text}"
        )

        return sha256(
            identity.encode("utf-8")
        ).hexdigest()
    
    def _remove_processing_metadata(self, metadata: dict) -> dict:
        processing_fields = {"blocks"}

        return {
            key:value
            for key, value in metadata.items()
            if key not in processing_fields
        }