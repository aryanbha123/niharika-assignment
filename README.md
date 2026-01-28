# AI Product-to-Code: Multi-Agent System

This project is a sophisticated multi-agent system, built with FastAPI and LangGraph, that transforms a high-level Product Request into structured Epics, User Stories, formal Specs, and finally, into validated, working code.

## Architecture Overview

The system uses a collection of specialized AI agents orchestrated by a LangGraph state machine. Each agent is responsible for a specific stage of the product development lifecycle, from initial planning to code validation.

- **FastAPI**: Provides the backend API, serves real-time updates via SSE, and handles user interactions.
- **LangGraph**: Orchestrates the agentic workflow, manages state, and enables pause/resume functionality through database checkpointing.
- **pgvector**: Stores all generated artifacts (epics, stories, specs) and provides semantic search capabilities.
- **Langfuse**: Offers complete observability and tracing for every LLM call, essential for debugging and cost management.
- **OpenAI**: The LLM provider used by the agents.

### Component Diagram
```mermaid
graph TD
    subgraph "Client"
        A[User/Client]
    end

    subgraph "API & Orchestration Layer (FastAPI + LangGraph)"
        B(FastAPI Backend)
        C(LangGraph State Machine)
        E(Checkpointing DB)
    end

    subgraph "Agent Fleet"
        F(Product Manager Agent)
        G(Lead Engineer Agent)
        H(System Architect Agent)
        I(Software Engineer Agent)
        J(QA Agent)
    end

    subgraph "Supporting Services"
        K(pgvector)
        L(Langfuse)
    end

    A -- "1. POST /workflow" --> B
    B -- "2. Invokes Graph" --> C
    A -- "3. POST /workflow/{id}/approve" --> B
    C -- "Persists/Resumes State" --> E
    F & G & H & I & J -- "Logs Traces" --> L
    H & I -- "Semantic Search" --> K
```

## Getting Started

Follow these instructions to get the project running locally.

### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- An OpenAI API Key
- A Langfuse account (optional, but recommended)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Configure Environment Variables
Create a `.env` file by copying the example.
```bash
cp .env.example .env
```
Now, edit the `.env` file and add your credentials:
```
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/mydb"
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
OPENAI_API_KEY="sk-..."
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Database
Start the PostgreSQL database with pgvector support using Docker Compose.
```bash
docker-compose up -d --build
```

### 5. Initialize the Database
Run the initialization script to create the necessary tables and extensions.
```bash
python init_db.py
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can view the OpenAPI documentation at `http://127.0.0.1:8000/docs`.

## Basic API Usage (Milestone 1 Demo)

1.  **Sign up a new user:**
    ```bash
    curl -X POST "http://127.0.0.1:8000/signup" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password123"}'
    ```

2.  **Log in to get an access token:**
    ```bash
    curl -X POST "http://127.0.0.1:8000/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=password123"
    ```
    *(You will get an `access_token` in the response. Copy it for the next step.)*

3.  **Start a new workflow:**
    ```bash
    TOKEN="your_access_token_here"
    curl -X POST "http://127.0.0.1:8000/workflow/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"request": "Build me a simple calculator app"}'
    ```
    *(This will return a `thread_id` for your workflow run.)*

4.  **Check the status of the workflow:**
    ```bash
    THREAD_ID="your_thread_id_here"
    curl -X GET "http://127.0.0.1:8000/workflow/$THREAD_ID/status" \
    -H "Authorization: Bearer $TOKEN"
    ```