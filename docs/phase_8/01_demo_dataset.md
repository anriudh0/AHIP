# Phase 8 Demo Dataset

AHIP uses deterministic sample data from `backend/seed_data.py` for product demos. The dataset is intentionally synthetic and supports healthcare operations review without real PHI.

## Demo Entities

| Type | Records | Demo Purpose |
|---|---:|---|
| Patients | 5 | Active, inactive, standard, medium, and high-risk member examples |
| Providers | 3 | In-network and out-of-network provider review |
| Benefit Plans | 2 | Authorization-required and non-authorization plan examples |
| Claims | 5 | Pended, submitted, and paid claim workflows |
| Care Tasks | 2 | Open care-task follow-up examples |
| Workflow Events | 2 | Claim and care-task timeline examples |

## Recommended Demo Cases

| Case ID | Scenario | What To Show |
|---|---|---|
| `CLM2001` | Pended claim from an out-of-network provider with missing contract context | Run case review, inspect risk queue, open case detail, review context and timeline |
| `CLM2002` | Submitted claim for a high-risk patient on an authorization-required plan | Explain benefit-plan context and deterministic recommendation behavior |
| `CLM2003` | Paid claim from an in-network facility | Show low-risk baseline behavior |
| `CLM2005` | Higher-value submitted claim for an active member | Show queue comparison and operational triage |

## Demo Safety Notes

- The dataset is synthetic and should not be described as real patient data.
- AHIP recommendations are operational decision-support outputs, not medical diagnosis or treatment guidance.
- Agent outputs are deterministic and auditable for demonstration stability.
