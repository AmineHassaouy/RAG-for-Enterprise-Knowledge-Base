# the first version will contain this structure:
``` 
advanced_rag/
│
├── ingestion/
│   ├── pdf_loader.py
│   │   └── PDFLoader
│   ├── web_loader.py
│   │   └── WebLoader
│   └── csv_loader.py
│       └── CSVLoader
│
├── processing/
│   ├── chunking.py
│   │   └── Chunker
│   └── metadata.py
│       └── MetadataProcessor
│
├── indexing/
│   └── vector_store.py
│       └── VectorStore
│
├── retrieval/
│   └── vector_retriever.py
│       └── VectorRetriever
│
├── generation/
│   ├── prompt.py
│   └── answer_generator.py
│       └── AnswerGenerator
│
└── app/
    └── streamlit_app.py
```

## the working workflow will be:
``` 
PDF/ Website / CSV
 ↓
Extract text
 ↓      
ingestion
 ↓
Chunk
 ↓
Create embeddings
 ↓
Store vectors
 ↓
User question
 ↓
Question embedding
 ↓
Similarity search
 ↓
Relevant chunks
 ↓
context
 ↓
LLM
 ↓
answer + source
 ↓
Streamlit
```