<div align="center">

# MERIDIAN
### Corporate SWOT Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<br>
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](#)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](#)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](#)
<br>
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](#)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)](#)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](#)
[![Nvidia](https://img.shields.io/badge/Nvidia_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](#)
[![Tavily](https://img.shields.io/badge/Tavily_Search-FF5722?style=for-the-badge)](#)

*An enterprise-grade, agentic Retrieval-Augmented Generation (RAG) system for producing automated financial SWOT analyses.*

</div>

---

## Table of Contents
- [Introduction](#introduction)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Introduction

The SWOT Intelligence Platform is a robust analytical engine designed for financial professionals. It fully automates the creation of comprehensive Strengths, Weaknesses, Opportunities, and Threats (SWOT) analyses for publicly traded companies. By extracting validated financial data directly from SEC 10-K filings and applying advanced large language models, it synthesizes deep, professional insights at unprecedented speed.

## Core Features

- **Automated Document Ingestion**: Seamlessly downloads and processes the latest SEC 10-K reports via the EDGAR API.
- **Precision Retrieval**: Utilizes Maximal Marginal Relevance (MMR) algorithms to extract the highest quality vector chunks from a PostgreSQL database.
- **Agentic Internet Fallback**: Features a deterministic logic layer that evaluates local context; if SEC data is insufficient, it autonomously queries the internet via the Tavily API to fill knowledge gaps.
- **Live Streaming Interface**: Employs Server-Sent Events (SSE) to deliver real-time progress updates and incremental generation directly to the frontend interface.
- **Dynamic PDF Reporting**: Compiles the final analysis into a structured, downloadable PDF report.

## System Architecture

The pipeline is structured around a highly performant, dual-stage retrieval and evaluation process.

![System Architecture Workflow](assets/flowchart.png)

1. **Data Acquisition**: Fetch SEC 10-K data from EDGAR.
2. **Vectorization**: Chunk the document into optimized sub-sections and embed using Nvidia's embedding models (`nv-embedqa-e5-v5`).
3. **Storage**: Persist vectors in a remote Supabase cluster using the PGVector extension.
4. **Context Evaluation**: When generating an analysis, the Nvidia NIM (`meta/llama-3.3-70b-instruct`) model evaluates the retrieved context against strict financial parameters.
5. **Fallback Execution**: If local context yields a "NO" on sufficiency, the system executes a targeted search across the web.
6. **Synthesis**: Final data from both the local Vector Store and the Internet is merged into formatted analytical summaries.

## Technology Stack

The platform is built on modern, scalable infrastructure and libraries:

### Backend & Core
- **Python 3.10+**: Core programming language.
- **FastAPI**: Asynchronous web framework for high-throughput API routing and SSE streaming.
- **LangChain Community**: Framework for document loaders, text splitters, and orchestration.

### Artificial Intelligence
- **Nvidia NIM**: Managed endpoints for ultra-fast Llama-3.3-70b instruction models.
- **Tavily Search API**: Search engine optimized specifically for LLM context retrieval.

### Database & Storage
- **Supabase**: Managed PostgreSQL cloud database.
- **PGVector**: PostgreSQL extension for high-dimensional vector similarity search.
- **SQLAlchemy**: ORM for relational database session management and cleanup operations.

## Getting Started

### Prerequisites
Before you begin, ensure you have the following credentials:
- Nvidia API Key
- Supabase Connection String (PostgreSQL)
- Tavily API Key

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd SWOT_ANALYSIS
   ```

2. **Initialize a Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Create a `.env` file at the project root and provide your access keys:

```ini
NVIDIA_API_KEY=your_nvidia_api_key_here
DATABASE_URL=postgresql://user:password@aws-0-region.pooler.supabase.com:5432/postgres
TAVILY_API_KEY=your_tavily_api_key_here
API_BASE=http://localhost:8000

# Model References
NVIDIA_LLM_MODEL=meta/llama-3.3-70b-instruct
NVIDIA_EMBED_MODEL=nvidia/nv-embedqa-e5-v5
```

## Usage

1. **Start the Production Server**
   Execute the server script to launch the FastAPI instance. This step automatically initializes database schemas if they do not exist.
   ```bash
   python server.py
   ```

2. **Access the Interface**
   Open a web browser and navigate to the application dashboard:
   `http://localhost:8000`

3. **Generate a Report**
   Input a company ticker or name, select the desired analytical categories, and monitor the live generation progress. Once completed, the final SWOT analysis can be downloaded as a PDF.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [Supabase](https://supabase.com/)
- [NVIDIA NIM](https://build.nvidia.com/)
- [Tavily](https://tavily.com/)
