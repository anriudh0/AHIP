# Phase 9 LinkedIn / Portfolio Write-up

I built AHIP, an AI Healthcare Intelligence Platform focused on healthcare operations workflows.

AHIP is a full-stack FastAPI, React, PostgreSQL, and Docker Compose project that demonstrates deterministic agentic workflow intelligence without relying on chatbots, RAG, vector databases, or external agent frameworks.

What I built:

- Healthcare data model for patients, providers, claims, benefit plans, contracts, workflow events, care tasks, agent memory, shared case memory, and audit logs
- Deterministic agents for patient journey, claims review, and provider contract review
- Typed context packs and relationship mapping
- Sequential multi-agent orchestration with shared case memory
- Consolidated recommendations, risk scoring, priority queue, and explainability notes
- Governance layer with audit logs, recommendation status workflow, manual overrides, and execution history
- React operations dashboard with executive metrics, risk queue, case detail view, evidence, context packs, relationship mapping, and agent timeline
- Productization docs, demo script, SaaS readiness notes, deployment checklist, roadmap, and final handover package

Healthcare concepts covered:

- Claim-to-provider relationship mapping
- Benefit-plan and authorization context
- Provider contract review
- Patient journey and care-task visibility
- Compliance and audit traceability
- Operations triage and escalation ownership

Engineering concepts covered:

- Clean FastAPI service structure
- SQLAlchemy data modeling
- Pydantic schemas
- React dashboard design
- Dockerized local deployment
- Deterministic agent pipelines
- Context engineering
- Human-in-the-loop governance

AHIP is intentionally not a diagnosis tool or autonomous adjudication system. It focuses on operational intelligence, explainability, and auditable human review.

This project helped me connect backend engineering, healthcare workflow design, product thinking, and responsible AI system boundaries into one portfolio-ready MVP.
