from dataclasses import dataclass, field

@dataclass
class Document: 
    text: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Chunk:
    test: str
    metadata: dict= field(default_factory=dict)