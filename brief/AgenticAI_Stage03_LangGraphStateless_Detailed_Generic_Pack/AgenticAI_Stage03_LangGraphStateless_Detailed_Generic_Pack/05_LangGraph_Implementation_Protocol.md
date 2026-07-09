# LangGraph Implementation Protocol

## Purpose

This protocol guides implementation of the stateless LangGraph stage.

## Implementation Steps

| Step | Action |
|---:|---|
| 1 | Review latest Repomix |
| 2 | Identify current agent workflow and orchestrator |
| 3 | Create graph folder/module |
| 4 | Define graph state schema |
| 5 | Create node wrappers around existing agents |
| 6 | Build graph with start/end and edges |
| 7 | Add graph runner service |
| 8 | Add new API endpoint for graph workflow |
| 9 | Keep existing deterministic endpoint unchanged |
| 10 | Add tests or smoke validation |
| 11 | Compare old vs graph output |
| 12 | Update README/completion report |
| 13 | Generate latest Repomix |

## Suggested Folder Structure

Python/FastAPI example:

```text
backend/app/application/graphs/
  __init__.py
  workflow_state.py
  workflow_graph.py
  graph_runner.py
  nodes/
    __init__.py
    context_node.py
    agent_1_node.py
    agent_2_node.py
    consolidator_node.py
    audit_node.py
```

## Dependency Guidance

Add LangGraph dependency only in this stage.

Example:

```text
langgraph
```

Pin version according to project compatibility if required.

## API Endpoint Pattern

Example:

```text
POST /api/v1/agents/run-case-review-graph
POST /api/recommendations/graph
POST /api/workflows/run-graph
```

Response should include:

| Field | Required |
|---|---|
| workflow_id / request_id | Yes |
| graph_mode | Yes |
| final_output / recommendation | Yes |
| agent_trace | Yes |
| shared_state / shared_context | Yes |
| explanation | If available |
| audit_reference | If available |
| comparison_note | Preferred |

## Avoid

| Avoid | Reason |
|---|---|
| Removing existing endpoint | Causes regression |
| Rewriting agent rules | Changes baseline |
| Adding LLM | Wrong stage |
| Adding checkpointing too early | Increases complexity |
| Returning only raw graph state | UI/reviewer needs readable output |
