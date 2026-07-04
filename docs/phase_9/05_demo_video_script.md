# Phase 9 Demo Video Script

Target duration: 4 to 6 minutes.

## 1. Opening

"This is AHIP, the AI Healthcare Intelligence Platform. AHIP helps healthcare operations teams identify workflow gaps, prioritize cases, and review auditable recommendations. It is not a chatbot, not a generic RAG application, and not a medical diagnosis tool."

## 2. Architecture Overview

"The platform uses a FastAPI backend, React frontend, PostgreSQL database, SQLAlchemy models, deterministic agents, typed context packs, shared case memory, risk scoring, and governance logs."

Show:

- README architecture summary
- Dashboard page

## 3. Run Case Review

"I will run a deterministic review for the sample claim `CLM2001`."

Show:

- Dashboard workflow action
- Run case review
- Explain that agent execution history is persisted

## 4. Risk Queue

"The consolidated recommendation appears in the Risk Queue with risk level, numeric score, priority, owner, and recommendation."

Show:

- Risk Queue
- Filters for case ID, risk, priority, and status

## 5. Case Detail

"The Case Detail page shows why the case was prioritized."

Show:

- Consolidated recommendation
- Evidence
- Explainability notes
- Claim context
- Patient journey context
- Compliance context
- Relationship mapping
- Agent timeline

## 6. Governance And Limitations

"AHIP keeps recommendations auditable and human-reviewed. The MVP uses synthetic data and lightweight RBAC. Production SaaS would require real authentication, tenant isolation, PHI controls, immutable audit retention, observability, and deployment hardening."

## 7. Closing

"AHIP demonstrates how deterministic agentic workflows can support healthcare operations intelligence with structured context, explainability, and governance."
