# AI Product-to-Code: Multi-Agent System

A FastAPI and LangGraph backend that runs a product request through a chain of AI agents: product manager, lead engineer, system architect, software engineer and QA. A human approves each step before the next agent runs.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## About

This was built as an assignment for Niharika; the brief is in `assignment.pdf`. Users sign up, create projects and start a workflow inside a project. A LangGraph state machine then hands the request through five GPT-4o agents. Each agent produces one artifact: epics, then user stories, then specs, then code, then a validation report. The graph pauses for approval between steps, and Langfuse traces every run.

This is an early milestone. Agent outputs are stored as raw LLM text inside placeholder structures. The knowledge-base search and the test run are simulated inside the prompts.

## Features

- **Auth**: signup with bcrypt-hashed passwords; login returns a JWT bearer token (OAuth2 password flow, 30-minute expiry).
- **Projects**: each user creates and lists their own projects. Workflows check that the caller owns the project.
- **Agent pipeline** (`agents/`, all using `gpt-4o` through `langchain-openai`):
  1. **Product Manager**: product request to epics
  2. **Lead Engineer**: epics to user stories with acceptance criteria
  3. **System Architect**: user stories to technical specs
  4. **Software Engineer**: specs to code artifacts (`generated/main.py`, `generated/test_main.py`)
  5. **QA**: code and specs to a validation report
- **Human in the loop**: after each agent, `should_continue` sends the graph to a `waitForApproval` node until the approve endpoint sets `approved: true`.
- **Checkpointing**: the graph is compiled with a Postgres checkpointer, so a run's state is stored under its `thread_id`.
- **Observability**: a Langfuse callback handler is attached to each workflow thread.
- **Optional document upload** when starting a workflow. Only the filename and content type are recorded.
- **Database schema** (`init_db.py`): `users`, `projects`, an `artifacts` table with a `vector(1536)` embedding column (pgvector), and LangGraph checkpoint tables.

## Tech Stack

| Layer | Tools |
|-------|-------|
| API | FastAPI, Uvicorn, Pydantic |
| Agents | LangGraph, LangChain, OpenAI (`gpt-4o`) |
| Auth | python-jose (JWT), passlib (bcrypt) |
| Database | PostgreSQL 16 with pgvector (`pgvector/pgvector:pg16`), psycopg2 |
| Tracing | Langfuse |

## Project Structure

```
.
├── main.py              # FastAPI app, mounts the routers
├── workflow.py          # LangGraph state machine and checkpointer
├── init_db.py           # Creates tables and extensions
├── agents/              # The five agent functions
├── routers/             # auth, users, projects, workflow endpoints
├── api/                 # DB connection, JWT helpers, Pydantic schemas
├── core/                # Settings (pydantic-settings) and Langfuse client
├── auth.md              # Auth endpoint reference
├── assignment.pdf       # Assignment brief
└── docker-compose.yml   # Postgres + pgvector
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- An OpenAI API key
- A Langfuse account (optional)

### 1. Environment Variables

Create a `.env` file in the project root with these variables:

| Variable | Notes |
|----------|-------|
| `DATABASE_URL` | Postgres connection string. Defaults to the local docker-compose database. |
| `OPENAI_API_KEY` | Required |
| `LANGFUSE_PUBLIC_KEY` | Langfuse project key |
| `LANGFUSE_SECRET_KEY` | Langfuse project key |
| `LANGFUSE_HOST` | Defaults to `https://cloud.langfuse.com` |

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install pydantic-settings python-dotenv   # imported by the code but missing from requirements.txt
```

### 3. Start the Database and Create the Tables

```bash
docker-compose up -d
python init_db.py
```

### 4. Run the API

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive docs are at `/docs`.

## API Endpoints

The workflow router is mounted with a `/workflow` prefix, and its own routes add a second segment. That is why the paths below contain `/workflow` twice. Every route except `/`, `/users/signup` and `/login` needs an `Authorization: Bearer <token>` header.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| POST | `/users/signup` | Register (`{"username", "password"}` as JSON) |
| POST | `/login` | Get a JWT (form-encoded `username`, `password`) |
| GET | `/users/me` | Current user |
| POST | `/projects/` | Create a project (`{"name"}`) |
| GET | `/projects/` | List your projects |
| POST | `/workflow/projects/{project_id}/workflow` | Start a workflow. Form fields: `request`, plus an optional `document` file. Returns a `thread_id`. |
| POST | `/workflow/workflow/{thread_id}/approve` | Approve the current step and resume the graph |
| GET | `/workflow/workflow/{thread_id}/status` | Current workflow state (epics, stories, specs, code, report) |

See [`auth.md`](auth.md) for request and response examples for the auth endpoints.

## Known Limitations

- The JWT `SECRET_KEY` is hard-coded in `api/auth.py`. Move it to an environment variable before any real deployment.
- The checkpointer connection string in `workflow.py` is hard-coded and does not read `DATABASE_URL`.
- `sse-starlette` is listed as a dependency, but no streaming endpoint exists yet.
- The `artifacts` table and its pgvector embedding column exist, but nothing writes to them or searches them yet.

## Author

**Aryan Bhandari**: [GitHub](https://github.com/aryanbha123)
