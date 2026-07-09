# Agent Node Mapping Guide

## Purpose

This guide helps interns map existing agents to graph nodes.

## Node Mapping Table

Complete this table before implementation.

| Existing Agent / Service | Current File | Current Method | Graph Node Name | State Input | State Output |
|---|---|---|---|---|---|
| Agent 1 |  |  |  |  |  |
| Agent 2 |  |  |  |  |  |
| Agent 3 |  |  |  |  |  |
| Consolidator / Recommendation |  |  |  |  |  |
| Explanation / Audit |  |  |  |  |  |

## Node Design Rule

A graph node should be thin.

It should:

```text
read state
call existing agent/service
write result back to state
return updated state
```

## Example Node Wrapper

```python
def passenger_intent_node(state: ABIPGraphState) -> ABIPGraphState:
    intent = normalize_intent(state["domain_input"])
    state["passenger_intent"] = intent
    state.setdefault("agent_outputs", []).append({
        "agent": "Passenger Intent Agent",
        "status": "completed",
        "output_summary": "Passenger request normalized",
        "details": intent,
    })
    return state
```

## Node Naming Rules

| Rule | Example |
|---|---|
| Use agent name clearly | `claims_review_node` |
| Keep node single-purpose | Do not combine unrelated agents |
| Avoid vague names | Avoid `process_node`, `ai_node` |
| Use domain language | `fare_rule_node`, `skill_gap_node` |
| Preserve sequence | Node order should match workflow logic |

## Edge Design

Start simple:

```text
START
→ context_builder_node
→ agent_1_node
→ agent_2_node
→ agent_3_node
→ consolidator_node
→ audit_node
→ END
```

Add conditional edges only if the current deterministic workflow already has meaningful branching.

Do not invent complex routing just to look advanced.
