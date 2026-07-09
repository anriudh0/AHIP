# API and UI Integration Guide

## Purpose

After LangGraph is implemented, the app should expose and optionally visualize graph execution.

## API Integration

Recommended:

| Endpoint | Purpose |
|---|---|
| Existing deterministic endpoint | Baseline workflow |
| New graph endpoint | LangGraph workflow |
| Existing audit/log endpoint | Evidence |
| Health endpoint | Deployment sanity |

## Response Alignment

Graph endpoint should return fields similar to the old endpoint so frontend impact is minimal.

| Old Response Field | Graph Response Field |
|---|---|
| recommended_offer / final_result | final_output / recommendation |
| agent_trace | agent_trace |
| structured_intent/context | shared_state/shared_context |
| explanation | explanation |
| audit_reference | audit_reference |

## UI Integration Options

| Option | When To Use |
|---|---|
| No UI change, API-only validation | If time is limited |
| Add toggle: Deterministic vs LangGraph | Best for demo |
| Add label: Graph Mode | Simple visible proof |
| Add Graph Execution panel | Best if Stage 1.5 console already exists |

## Recommended UI Enhancement

Add a toggle or badge in Agent Workflow Console:

```text
Mode: Deterministic / LangGraph
```

When LangGraph mode is selected:

```text
Run Graph Workflow
→ show same timeline/context/output
→ add Graph Execution note
```

## UI Copy

Use:

```text
LangGraph Stateless Mode
```

Avoid:

```text
Fully autonomous AI
LLM-powered reasoning
Self-learning graph
```

## Validation

Confirm:

| Check | Required |
|---|---|
| Existing UI still works | Yes |
| Graph endpoint can be called | Yes |
| Graph output can be displayed | Preferred |
| Graph mode does not break old mode | Yes |
| Graph output matches old workflow | Yes |
