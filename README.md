# AHIP

AI Healthcare Intelligence Platform is a FastAPI and React application for deterministic healthcare operations intelligence.

## Current Scope

- Patient, provider, claim, benefit, workflow, and agent audit data models
- FastAPI backend with versioned API routes
- React frontend for dashboard, risk queue, case detail, patients, claims, and providers
- Phase 2 deterministic healthcare agents:
  - Patient Journey Agent
  - Claims Review Agent
  - Provider Contract Agent
- Structured agent outputs and persisted agent execution history
- Context packs, relationship mapping, shared case memory, decision recommendations, governance audit, and dashboard workflows

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

## Phase 8 Demo Documentation

AHIP is demo-ready as a healthcare operations SaaS MVP using synthetic data and deterministic agent workflows.

- [Demo Dataset](docs/phase_8/01_demo_dataset.md)
- [Demo Script](docs/phase_8/02_demo_script.md)
- [Product Walkthrough](docs/phase_8/03_product_walkthrough.md)
- [SaaS Readiness Notes](docs/phase_8/04_saas_readiness.md)
- [Deployment Checklist](docs/phase_8/05_deployment_checklist.md)
- [Known Limitations](docs/phase_8/06_known_limitations.md)
