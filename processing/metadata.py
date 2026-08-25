from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

class MetadataValidator:
    """Validates and standardizes metadata for documents and chunks."""

    # Default metadata schema for documents
    DOCUMENT_SCHEMA = {
        "source": str,
        "type": str,
        "title": Optional[str],
        "author": Optional[str],
        "timestamp": Optional[str],  # ISO format (e.g., "2026-08-25T12:00:00")
        "language": Optional[str],
        "custom_fields": Optional[Dict[str, Any]]
    }

    # Default metadata schema for chunks
    CHUNK_SCHEMA = {
        **DOCUMENT_SCHEMA,
        "chunk_index": int,
        "total_chunks": int,
        "chunk_id": Optional[str]  # Unique identifier for the chunk
    }

    @staticmethod
    def validate_metadata(metadata: Dict[str, Any], schema: Dict[str, type]) -> bool:
        """
        Validate metadata against a schema.

        Args:
            metadata: Dictionary of metadata to validate.
            schema: Dictionary defining the expected types for each key.

        Returns:
            bool: True if metadata is valid, False otherwise.
        """
        for key, expected_type in schema.items():
            if key in metadata:
                if not isinstance(metadata[key], expected_type):
                    return False
        return True

    @staticmethod
    def standardize_metadata(
        metadata: Dict[str, Any],
        schema: Dict[str, type],
        default_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Standardize metadata by ensuring all required keys are present and of the correct type.
        Missing keys are filled with default values.

        Args:
            metadata: Dictionary of metadata to standardize.
            schema: Dictionary defining the expected types for each key.
            default_values: Dictionary of default values for missing keys.

        Returns:
            Dict[str, Any]: Standardized metadata.
        """
        standardized = metadata.copy()
        default_values = default_values or {}

        for key, expected_type in schema.items():
            if key not in standardized:
                standardized[key] = default_values.get(key, None)
            else:
                # Convert to the expected type if possible
                if not isinstance(standardized[key], expected_type):
                    try:
                        standardized[key] = expected_type(standardized[key])
                    except (ValueError, TypeError):
                        standardized[key] = default_values.get(key, None)

        return standardized

    @staticmethod
    def generate_chunk_id() -> str:
        """Generate a unique ID for a chunk."""
        return str(uuid.uuid4())

    @staticmethod
    def add_timestamp(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Add a timestamp to the metadata if not already present."""
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.now().isoformat()
        return metadata

class MetadataEnricher:
    """Enriches metadata with additional fields (e.g., derived from content or external sources)."""

    @staticmethod
    def enrich_with_title(metadata: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Add a title to metadata if not present (e.g., first line of text)."""
        if "title" not in metadata and text:
            metadata["title"] = text.split("\n")[0][:100]  # Use first line as title
        return metadata

    @staticmethod
    def enrich_with_language(metadata: Dict[str, Any], text: str, default_language: str = "en") -> Dict[str, Any]:
        """Add a language field to metadata (placeholder for actual language detection)."""
        if "language" not in metadata:
            metadata["language"] = default_language
        return metadata

    @staticmethod
    def enrich_with_chunk_info(
        metadata: Dict[str, Any],
        chunk_index: int,
        total_chunks: int
    ) -> Dict[str, Any]:
        """Add chunk-specific metadata."""
        metadata["chunk_index"] = chunk_index
        metadata["total_chunks"] = total_chunks
        metadata["chunk_id"] = MetadataValidator.generate_chunk_id()
        return metadata

# Example usage
if __name__ == "__main__":
    # Example metadata
    doc_metadata = {
        "source": "example.txt",
        "type": "text",
        "author": "John Doe"
    }

    # Validate metadata
    is_valid = MetadataValidator.validate_metadata(doc_metadata, MetadataValidator.DOCUMENT_SCHEMA)
    print(f"Is metadata valid? {is_valid}")

    # Standardize metadata
    standardized_metadata = MetadataValidator.standardize_metadata(
        doc_metadata,
        MetadataValidator.DOCUMENT_SCHEMA,
        default_values={"timestamp": datetime.now().isoformat(), "language": "en"}
    )
    print(f"Standardized metadata: {standardized_metadata}")

    # Enrich metadata
    enriched_metadata = MetadataEnricher.enrich_with_title(standardized_metadata, "This is a title.\n\nThis is content.")
    print(f"Enriched metadata: {enriched_metadata}")