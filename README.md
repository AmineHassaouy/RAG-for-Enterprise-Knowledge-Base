Enterprise Knowledge Base — Multi-Source RAG

«An extensible Retrieval-Augmented Generation (RAG) system designed to turn enterprise documents and external data sources into a searchable knowledge base with grounded, source-cited answers.»

Overview

Enterprise information is often distributed across PDFs, websites, CSV files, and other structured or unstructured sources. Finding reliable information across these sources can be slow and inefficient.

This project aims to build a modular Retrieval-Augmented Generation (RAG) pipeline that ingests information from multiple sources, transforms it into searchable representations, retrieves the most relevant context for a user's question, and generates an answer grounded in the retrieved data.

The long-term goal is to provide a web-based interface where users can:

- Upload documents
- Provide website sources
- Connect structured datasets
- Ask questions using natural language
- Receive context-aware answers
- Inspect the sources used to generate each answer

Architecture

The system is organized into independent stages:

┌──────────────────────────────┐
│        Data Sources          │
│  PDF · Web · CSV · Database │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Ingestion           │
│   Extract & normalize data   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Processing           │
│   Chunking · Metadata        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Indexing            │
│      Embeddings · Vectors    │
└──────────────┬───────────────┘
               │
               ▼
        ┌───────────────┐
        │ Vector Store  │
        └───────┬───────┘
                │
        User Question
                │
                ▼
┌──────────────────────────────┐
│          Retrieval            │
│ Query embedding + similarity │
│ search + relevant context    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Generation           │
│    Context + Prompt + LLM    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Answer             │
│     + Source Citations       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Streamlit Interface    │
└──────────────────────────────┘

Project Structure

RAG-for-Enterprise-Knowledge-Base/
│
├── ingestion/
│   ├── pdf_loader.py
│   ├── web_loader.py
│   └── csv_loader.py
│
├── processing/
│   ├── chunking.py
│   └── metadata.py
│
├── indexing/
│   └── vector_store.py
│
├── retrieval/
│   └── vector_retriever.py
│
├── generation/
│   ├── prompt.py
│   └── answer_generator.py
│
├── config.py
├── requirements.txt
├── .gitignore
└── README.md

Core Components

1. Ingestion

Responsible for extracting information from different data sources.

Current architecture includes dedicated loaders for:

- PDF documents
- Web pages
- CSV files

Each loader is designed to isolate source-specific extraction logic from the rest of the RAG pipeline.

2. Processing

The extracted information is transformed into a format suitable for retrieval.

This stage handles:

- Text chunking
- Metadata extraction and normalization
- Document organization
- Preparation for embedding generation

3. Indexing

Processed chunks are converted into vector representations and stored in a vector database/store.

This enables semantic similarity search rather than relying exclusively on exact keyword matching.

4. Retrieval

When a user submits a question:

1. The question is converted into an embedding.
2. Similarity search is performed against the indexed knowledge base.
3. The most relevant chunks are retrieved.
4. Retrieved content is passed to the generation layer as context.

5. Generation

The generation layer combines:

User Question
      +
Retrieved Context
      +
Prompt
      ↓
     LLM
      ↓
Grounded Answer

The objective is to generate answers based on the retrieved knowledge rather than relying solely on the model's internal knowledge.

6. Application Layer

The planned user interface uses Streamlit to provide an interactive environment for:

- Data ingestion
- Knowledge-base querying
- Answer generation
- Source inspection

Design Principles

The project is being developed around several engineering principles:

Modularity

Each stage of the RAG pipeline has a dedicated responsibility, making individual components easier to test, replace, and extend.

Separation of Concerns

Data extraction, processing, indexing, retrieval, and generation are intentionally separated rather than implemented as one large pipeline.

Source Grounding

Generated answers should be supported by retrieved information and accompanied by source references whenever possible.

Extensibility

The architecture is designed to make it possible to add new:

- Data loaders
- Chunking strategies
- Embedding models
- Vector stores
- Retrieval strategies
- LLM providers
- User interfaces

without restructuring the entire application.

Current Development Status

This repository is under active development.

The current focus is building the core RAG infrastructure incrementally, starting from ingestion and processing and progressing toward indexing, retrieval, generation, and the final application layer.

Planned Development

- [x] Project architecture
- [x] Modular ingestion layer
- [x] PDF ingestion
- [x] Web ingestion
- [x] CSV ingestion
- [ ] Advanced document processing
- [ ] Embedding pipeline
- [ ] Vector store integration
- [ ] Semantic retrieval
- [ ] Context-aware generation
- [ ] Source citation pipeline
- [ ] Streamlit interface
- [ ] Database connectors
- [ ] Retrieval evaluation
- [ ] RAG evaluation and benchmarking
- [ ] Production deployment

Installation

Clone the repository:

git clone https://github.com/AmineHassaouy/RAG-for-Enterprise-Knowledge-Base.git
cd RAG-for-Enterprise-Knowledge-Base

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Usage

The project is currently being developed component by component.

Once the application layer is completed, the intended workflow will be:

1. Add knowledge sources
        ↓
2. Extract and process content
        ↓
3. Generate embeddings
        ↓
4. Build/update the vector index
        ↓
5. Ask a natural-language question
        ↓
6. Retrieve relevant context
        ↓
7. Generate a grounded answer
        ↓
8. Inspect the supporting sources

Example Use Cases

The architecture can be adapted to enterprise knowledge bases such as:

- Internal company documentation
- Technical documentation
- HR knowledge bases
- Legal document collections
- Research repositories
- Product documentation
- Customer support knowledge bases
- Educational resources
- Internal policies and procedures

Technology Stack

The project is built around a Python-based RAG architecture and is designed to integrate technologies such as:

Layer| Technology
Language| Python
Application| Streamlit
Document Processing| Python-based loaders
Embeddings| Configurable
Vector Search| Configurable
LLM| Configurable
Data Sources| PDF, Web, CSV, Database
Architecture| Modular RAG

Specific implementations may evolve as the project develops.

Why This Project?

This project focuses not only on building a chatbot, but on understanding the engineering required to build a production-oriented RAG system.

The main objectives are to explore:

- Multi-source data ingestion
- Document processing
- Chunking strategies
- Metadata management
- Embedding pipelines
- Vector search
- Retrieval strategies
- Prompt engineering
- Grounded generation
- Source attribution
- Modular AI system architecture
- RAG evaluation

Roadmap

Ingestion
   ↓
Processing
   ↓
Embeddings
   ↓
Vector Store
   ↓
Retrieval
   ↓
Generation
   ↓
Source Attribution
   ↓
Evaluation
   ↓
Web Application
   ↓
Production Deployment

Author

Amine Hassaouy

AI & Data Science / Engineering

GitHub: "@AmineHassaouy" (https://github.com/AmineHassaouy)

---

License

This project is currently under development. License information will be added as the project matures.