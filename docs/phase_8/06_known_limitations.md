# Phase 8 Known Limitations

## Product Limitations

- AHIP is an MVP demo, not a production SaaS platform.
- The dataset is synthetic and limited.
- The dashboard is designed for demonstration workflows, not full enterprise operations coverage.
- Relationship mapping is shown as structured data rather than an interactive graph visualization.

## Agent Limitations

- Agents are deterministic rule-based services.
- No LLM, RAG, vector database, LangGraph, CrewAI, or AutoGen functionality is used.
- Recommendations are operational workflow suggestions and require human review.
- AHIP does not make diagnosis, treatment, or autonomous adjudication decisions.

## Governance Limitations

- RBAC is lightweight and uses mock role headers.
- Audit logging is suitable for MVP traceability, not immutable compliance-grade retention.
- Manual override capture exists, but production approval workflows are not implemented.

## SaaS Limitations

- No real tenant isolation.
- No production authentication provider.
- No production secrets management workflow.
- No production monitoring, alerting, or backup policy.
- Docker Compose is for local/demo orchestration, not a complete production deployment model.
