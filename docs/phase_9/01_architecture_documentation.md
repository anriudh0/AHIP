# Phase 9 Architecture Documentation

## System Overview

AHIP is a healthcare operations intelligence MVP. It combines structured healthcare data, deterministic agents, context engineering, shared case memory, risk scoring, governance logging, and a React dashboard into one auditable workflow.

AHIP does not use chatbots, LLM integrations, RAG, vector databases, LangGraph, CrewAI, or AutoGen.

## High-Level Architecture

```text
React Dashboard
  -> FastAPI Routes
    -> Application Services
      -> Context Builder
      -> Deterministic Agents
      -> Workflow Orchestrator
      -> Consolidator Agent
      -> Recommendation Engine
      -> Governance Service
    -> SQLAlchemy Models
      -> PostgreSQL
```

## Backend Layers

| Layer | Responsibility |
|---|---|
| API | FastAPI routes for health, patients, providers, claims, dashboard, agents, context, queue, governance |
| Application | Agent orchestration, context building, risk scoring, recommendations, governance services |
| Domain | SQLAlchemy entities and Pydantic schemas |
| Infrastructure | Database session and initialization |

## Frontend Layers

| Layer | Responsibility |
|---|---|
| API Client | Calls existing FastAPI endpoints |
| Types | Frontend data contracts for dashboard, context, recommendations, timeline |
| Components | Metric cards, status badges, agent timeline |
| Pages | Dashboard, Risk Queue, Case Detail, Claims, Patients, Providers |

## Healthcare Data Model

AHIP models operational healthcare entities:

- Patient
- Provider
- Claim
- BenefitPlan
- ProviderContract
- CareTask
- WorkflowEvent
- AgentExecution
- AgentMemory
- SharedCaseMemory
- AuditLog

## Agent Pipeline

1. User runs a case review.
2. Context builder creates typed context packs.
3. Patient Journey Agent evaluates patient and care-task context.
4. Claims Review Agent evaluates claim and benefit-plan context.
5. Provider Contract Agent evaluates provider and contract context.
6. Workflow Orchestrator passes shared memory across agents.
7. Consolidator Agent creates a consolidated recommendation.
8. Recommendation Engine scores risk and priority from the consolidated output.
9. Governance layer records audit events, statuses, overrides, and execution history.

## Dashboard Flow

1. Dashboard displays executive and operational metrics.
2. Risk Queue displays prioritized recommendations.
3. Case Detail displays evidence, explainability, context packs, relationships, and agent timeline.
4. Governance endpoints support execution history and recommendation workflow visibility.

## Deployment

AHIP runs locally through Docker Compose:

- PostgreSQL database
- FastAPI backend
- React/Vite frontend

Docker Compose is suitable for MVP demonstration, not full production deployment.
