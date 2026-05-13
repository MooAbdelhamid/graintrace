# GrainTrace

AI-powered retrieval and traceability system for identifying musical bows made from protected timber wood.

---

# Project Overview

The Timber Bow Identification System is a retrieval-based AI system designed to identify and verify musical bows using image embeddings and similarity search.

The system generates embedding vectors from bow images and compares them against a vector database to determine whether a queried bow matches an already registered bow.

In addition to similarity retrieval, the system supports ownership traceability and contract verification through a metadata management system.

The project is designed using a modular service-oriented architecture to support scalability, maintainability, and future extensions such as multispectral imaging and blockchain integration.

---

# Core Features

- Bow image registration
- Image preprocessing and validation
- Embedding generation using deep learning
- Vector similarity retrieval
- Ownership and contract traceability
- Top-k similarity search
- Modular API-based architecture
- Extensible service-oriented design

---

# System Architecture

<img src="docs/images/architecture.png" width="1000">

The system consists of:
- User Interface (UI)
- Data Flow Manager / Orchestrator
- Preprocessing & Validation Service
- Embedding Model Service
- Retrieval Service
- Vector Database
- Metadata Service
- Metadata Database

Detailed architecture documentation can be found in:

```plaintext
docs/system_design.md
```

---

# Technology Stack

## Backend
- FastAPI

## Machine Learning
- PyTorch

## Vector Database
- Qdrant

## Metadata Database
- PostgreSQL

## Frontend
- Streamlit

## Containerization
- Docker

---

# License

TBD

---

# Contributors

TBD