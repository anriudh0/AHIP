# Phase 9 Future Roadmap

This roadmap describes responsible next steps after the MVP. It does not claim these capabilities are already implemented.

## Near-Term Product Hardening

- Improve seeded demo scenarios and reset scripts.
- Add richer empty states and loading states.
- Add screenshot assets to a tracked `screenshots/` folder when final images are selected.
- Add focused frontend tests for dashboard navigation and queue filtering.
- Expand backend tests around governance and recommendation workflow edge cases.

## SaaS Readiness

- Add production authentication through an identity provider.
- Replace mock role headers with tenant-aware RBAC.
- Add organization and tenant scoping.
- Add secrets management.
- Add deployment environments for development, staging, and production.
- Add backup, restore, and data retention procedures.

## Healthcare Integration Readiness

- Map claim data toward EDI 837-style concepts.
- Explore FHIR-aligned patient and task representations.
- Add import/export boundaries for payer operations systems.
- Add data quality validation before agent evaluation.

## Governance And Compliance

- Add immutable audit retention.
- Add approval workflow for recommendation overrides.
- Add governance reports for compliance review.
- Add least-privilege role policy testing.

## Platform Operations

- Add observability for API latency, queue health, error rates, and agent execution failures.
- Add structured logs and tracing.
- Add background job processing if long-running workflows are introduced.

## Agentic AI Evolution

AHIP should remain deterministic for the current MVP. Any future AI expansion must preserve:

- Structured inputs
- Explainable outputs
- Human review
- Auditability
- PHI safety
- Clear non-diagnostic boundaries
