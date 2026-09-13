from abc import ABC, abstractmethod

from ingestion.document import Document, Chunk


class Chunker(ABC):

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        pass


class RecursiveChunker(Chunker):

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: Document) -> list[Chunk]:
        if not document.text:
            return []

        text_chunks = self._split_text(document.text)

        return [
            Chunk(
                text=text,
                metadata=document.metadata.copy()
            )
            for text in text_chunks
        ]

    def _split_text(self, text: str) -> list[str]:
        if len(text) <= self.chunk_size:
            return [text]

        separators = ["\n\n", "\n", ". ", " ", ""]

        return self._recursive_split(text, separators)

    def _recursive_split(
        self,
        text: str,
        separators: list[str]
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text]

        if not separators:
            return self._split_by_size(text)

        separator = separators[0]

        if separator == "":
            pieces = list(text)
        else:
            pieces = text.split(separator)

        chunks = []
        current = ""

        for piece in pieces:
            candidate = (
                piece
                if not current
                else current + separator + piece
            )

            if len(candidate) <= self.chunk_size:
                current = candidate
                continue

            if current:
                chunks.append(current)

            if len(piece) > self.chunk_size:
                chunks.extend(
                    self._recursive_split(
                        piece,
                        separators[1:]
                    )
                )
                current = ""
            else:
                current = piece

        if current:
            chunks.append(current)

        return self._add_overlap(chunks)

    def _split_by_size(self, text: str) -> list[str]:
        return [
            text[i:i + self.chunk_size]
            for i in range(0, len(text), self.chunk_size)
        ]

    def _add_overlap(self, chunks: list[str]) -> list[str]:
        if self.overlap <= 0 or len(chunks) <= 1:
            return chunks

        result = [chunks[0]]

        for i in range(1, len(chunks)):
            previous = chunks[i - 1]
            overlap_text = previous[-self.overlap:]

            result.append(
                overlap_text + chunks[i]
            )

        return result


class StructuralChunker(Chunker):

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.fallback_chunker = RecursiveChunker(
            chunk_size=chunk_size,
            overlap=overlap
        )

    def chunk(self, document: Document) -> list[Chunk]:
        blocks = document.metadata.get("blocks", [])

        if not blocks:
            return self.fallback_chunker.chunk(document)

        sections = self._build_sections(blocks)

        chunks = []

        for section in sections:
            section_text = section["text"]

            if len(section_text) <= self.chunk_size:
                chunks.append(
                    Chunk(
                        text=section_text,
                        metadata={
                            **document.metadata,
                            "section": section.get("heading")
                        }
                    )
                )
            else:
                section_document = Document(
                    text=section_text,
                    metadata={
                        **document.metadata,
                        "section": section.get("heading")
                    }
                )

                chunks.extend(
                    self.fallback_chunker.chunk(
                        section_document
                    )
                )

        return chunks

    def _build_sections(self, blocks: list[dict]) -> list[dict]:
        sections = []

        current_heading = None
        current_content = []

        for block in blocks:

            if block["type"] == "heading":

                if current_content:
                    sections.append(
                        {
                            "heading": current_heading,
                            "text": "\n\n".join(current_content)
                        }
                    )

                current_heading = block["text"]
                current_content = [block["text"]]

            else:
                current_content.append(block["text"])

        if current_content:
            sections.append(
                {
                    "heading": current_heading,
                    "text": "\n\n".join(current_content)
                }
            )

        return sections