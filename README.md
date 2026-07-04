# AHIP

AI Healthcare Intelligence Platform is a FastAPI and React application for deterministic healthcare operations intelligence.

## Current Scope

- Patient, provider, claim, benefit, workflow, and agent audit data models
- FastAPI backend with versioned API routes
- React frontend for dashboard, patients, claims, and providers
- Phase 2 deterministic healthcare agents:
  - Patient Journey Agent
  - Claims Review Agent
  - Provider Contract Agent
- Structured agent outputs and persisted agent execution history

## Phase 2 Agent Behavior

The Phase 2 agents do not use LLMs, chatbots, vector databases, RAG, or external agent frameworks. Each agent accepts structured healthcare context, applies deterministic business rules, returns a structured output, and logs execution history through the existing database models.

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
python -m pytest app\tests
```

## Docker

```bash
docker compose up --build
```
