# Graph State Design Guide

## Purpose

Graph state is the shared object passed through LangGraph nodes.

It replaces hidden implicit context with explicit state.

## Generic State Shape

```python
from typing import Any, Dict, List, Optional, TypedDict

class WorkflowGraphState(TypedDict, total=False):
    workflow_id: str
    domain_input: Dict[str, Any]
    shared_context: Dict[str, Any]
    agent_outputs: List[Dict[str, Any]]
    final_recommendation: Dict[str, Any]
    explanation: str
    audit_reference: Optional[str]
    errors: List[str]
```

## State Design Rules

| Rule | Requirement |
|---|---|
| Keep it explicit | State fields should be easy to understand |
| Keep it serializable | JSON-compatible values preferred |
| Keep domain names | Use candidate/passenger/case/claim terms based on project |
| Avoid secrets | Never put keys/secrets in graph state |
| Avoid raw huge payloads | Store only useful context |
| Preserve trace | Agent outputs should be retained |
| Support comparison | State should map back to old workflow response |

## Project-Specific Examples

### CPIP

```python
class CPIPGraphState(TypedDict, total=False):
    workflow_id: str
    candidate_profile: Dict[str, Any]
    target_role: Dict[str, Any]
    skill_gap_result: Dict[str, Any]
    portfolio_result: Dict[str, Any]
    resume_result: Dict[str, Any]
    role_match_result: Dict[str, Any]
    recommendation: Dict[str, Any]
    explanation: str
    audit_reference: str
```

### ABIP

```python
class ABIPGraphState(TypedDict, total=False):
    request_id: str
    passenger_intent: Dict[str, Any]
    flight_offers: List[Dict[str, Any]]
    fare_rule_result: List[Dict[str, Any]]
    risk_result: List[Dict[str, Any]]
    recommended_offer: Dict[str, Any]
    explanation: str
    audit_reference: str
```

### AHIP

```python
class AHIPGraphState(TypedDict, total=False):
    case_id: str
    claim_context: Dict[str, Any]
    patient_journey_output: Dict[str, Any]
    claims_review_output: Dict[str, Any]
    provider_contract_output: Dict[str, Any]
    shared_case_memory: Dict[str, Any]
    consolidated_output: Dict[str, Any]
    audit_reference: str
```

## Minimum State Validation

Before closing the stage, confirm:

| Check | Required |
|---|---|
| State starts with domain input | Yes |
| Every node updates state | Yes |
| Final state includes recommendation/output | Yes |
| Agent outputs are preserved | Yes |
| Explanation/audit included if available | Yes |
| State can be serialized to JSON | Yes |
