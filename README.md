# AHIP - AI Healthcare Intelligence Platform

AHIP is a deterministic healthcare operations intelligence platform built with FastAPI, React, PostgreSQL, and Docker Compose. It uses specialized rule-based agents, typed context packs, shared case memory, recommendation scoring, governance logging, and an operations dashboard to surface healthcare workflow gaps and recommend auditable next actions.

AHIP is not a chatbot, not a generic RAG application, and not a medical diagnosis or treatment system.

## What AHIP Demonstrates

- Healthcare operations data model for patients, providers, claims, benefit plans, contracts, workflow events, care tasks, agent memory, shared case memory, and audit logs.
- Deterministic agents for patient journey review, claims review, and provider contract review.
- Context builder and context packs for claim, patient journey, compliance, and relationship mapping.
- Sequential multi-agent orchestration with shared case memory and consolidated recommendations.
- Risk scoring, escalation ownership, priority queue, explainability notes, and recommendation workflow.
- Governance foundation with audit logs, manual override capture, recommendation status updates, execution history, and role-based access checks.
- React operations dashboard with executive metrics, risk queue, case detail view, evidence, context, relationships, and agent timeline.

## Architecture Summary

| Layer | Implementation |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| Database | PostgreSQL with SQLAlchemy models |
| Agent Layer | Deterministic Python services |
| Context Layer | Typed Pydantic context packs |
| Decision Layer | Rule-based risk scoring and recommendation queue |
| Governance Layer | Audit logs, status workflow, overrides, execution history |
| Deployment | Docker Compose |

## Repository Structure

```text
backend/
  app/
    api/v1/routes/
    application/agents/
    application/context/
    application/decision/
    application/governance/
    domain/entities/
    domain/schemas/
    infrastructure/database/
frontend/
  src/api/
  src/components/
  src/pages/
docs/
  phase_8/
  phase_9/
```

## Local Setup

Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Docker:

```bash
docker compose up --build
```

Frontend URL:

```text
http://localhost:5173
```

Backend API docs:

```text
http://localhost:8000/docs
```

## Demo Path

1. Start the app with Docker Compose.
2. Open the dashboard.
3. Run the deterministic case review for `CLM2001`.
4. Open the Risk Queue.
5. Click the case detail view.
6. Review recommendation, evidence, explainability notes, context packs, relationship mapping, and agent timeline.
7. Explain governance and human-in-the-loop review boundaries.

## Validation

Frontend:

```bash
cd frontend
npm run build
```

Backend:

```bash
cd backend
python -m compileall app
```

Backend tests, if dependencies are installed:

```bash
cd backend
python -m pytest app\tests
```

## Documentation

Phase 8 productization:

- [Demo Dataset](docs/phase_8/01_demo_dataset.md)
- [Demo Script](docs/phase_8/02_demo_script.md)
- [Product Walkthrough](docs/phase_8/03_product_walkthrough.md)
- [SaaS Readiness Notes](docs/phase_8/04_saas_readiness.md)
- [Deployment Checklist](docs/phase_8/05_deployment_checklist.md)
- [Known Limitations](docs/phase_8/06_known_limitations.md)

Phase 9 final handover:

- [Architecture Documentation](docs/phase_9/01_architecture_documentation.md)
- [Product Brief](docs/phase_9/02_product_brief.md)
- [Future Roadmap](docs/phase_9/03_future_roadmap.md)
- [LinkedIn / Portfolio Write-up](docs/phase_9/04_linkedin_portfolio_post.md)
- [Demo Video Script](docs/phase_9/05_demo_video_script.md)
- [Screenshots Package](docs/phase_9/06_screenshots_package.md)

## Known Limitations

- Demo data is synthetic and limited.
- Agents are deterministic rule-based services, not LLM agents.
- RBAC is lightweight and suitable for MVP demonstration only.
- There is no real tenant isolation, production authentication provider, immutable audit store, or production observability stack.
- AHIP recommendations are operational decision-support outputs and require human review.
