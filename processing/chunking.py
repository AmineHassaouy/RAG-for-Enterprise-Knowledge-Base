from typing import List, Optional
import re

class TextChunk:
    """Represents a chunk of text with associated metadata."""

    def __init__(self, text: str, metadata: Optional[dict] = None):
        self.text = text
        self.metadata = metadata if metadata else {}

    def __repr__(self):
        return f"TextChunk(text={self.text[:50]}..., metadata={self.metadata})"

class TextChunking:
    """Splits text into chunks of a specified size."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200, separator: str = "\n\n"):
        """
        Args:
            chunk_size: Maximum size of each chunk (in characters).
            overlap: Number of characters to overlap between chunks.
            separator: String used to split the text (e.g., "\n\n" for paragraphs).
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks based on the separator and chunk size."""
        if not text:
            return []

        # Split text into paragraphs or sentences
        segments = text.split(self.separator)
        chunks = []
        current_chunk = ""

        for segment in segments:
            if not segment:
                continue

            # Check if adding the segment exceeds the chunk size
            if len(current_chunk) + len(segment) + len(self.separator) <= self.chunk_size:
                current_chunk += (self.separator + segment).strip()
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = segment

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def chunk_document(self, document: 'Document') -> List[TextChunk]:
        """
        Split a Document into chunks and preserve metadata.

        Args:
            document: A Document object with `text` and `metadata` attributes.

        Returns:
            List of TextChunk objects.
        """
        chunks = self.chunk_text(document.text)
        return [
            TextChunk(
                text=chunk,
                metadata={
                    **document.metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
            for i, chunk in enumerate(chunks)
        ]

    def chunk_documents(self, documents: List['Document']) -> List[TextChunk]:
        """Split a list of Document objects into chunks."""
        all_chunks = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks