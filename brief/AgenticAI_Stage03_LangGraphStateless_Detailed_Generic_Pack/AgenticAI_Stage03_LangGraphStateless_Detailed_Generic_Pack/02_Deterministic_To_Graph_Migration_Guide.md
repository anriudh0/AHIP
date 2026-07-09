# Deterministic to Graph Migration Guide

## Purpose

This guide explains how to migrate from manual deterministic orchestration to graph orchestration without breaking the MVP.

## Before LangGraph

Most projects currently work like this:

```text
API endpoint
→ Orchestrator function
→ Agent 1
→ Agent 2
→ Agent 3
→ Final result
```

## After LangGraph

The project should work like this:

```text
API endpoint
→ Graph runner
→ Node 1
→ Node 2
→ Node 3
→ Final state
→ Response
```

## Migration Principle

Do not rewrite agent logic.

Wrap existing functions/classes as graph nodes.

| Existing Item | LangGraph Equivalent |
|---|---|
| Agent class/function | Node function |
| Shared context dict/object | Graph state |
| Orchestrator sequence | Graph edges |
| Final response builder | Final graph output |
| Audit logging | Existing audit/logging node or post-run action |
| UI trace | Graph execution trace or same agent trace format |

## Recommended Migration Path

| Step | Action |
|---:|---|
| 1 | Identify current main workflow endpoint |
| 2 | Identify current orchestrator |
| 3 | List all agent calls in sequence |
| 4 | Define graph state schema |
| 5 | Create one node wrapper per agent |
| 6 | Add edges in same sequence |
| 7 | Add graph runner service |
| 8 | Add graph API endpoint |
| 9 | Compare graph response with existing response |
| 10 | Capture evidence and Repomix |

## Keep Old API Working

Do not remove the existing deterministic endpoint.

Recommended approach:

| Endpoint | Purpose |
|---|---|
| Existing endpoint | Keeps original MVP stable |
| New graph endpoint | Demonstrates LangGraph evolution |

Example:

```text
POST /api/workflow/run
POST /api/workflow/run-graph
```

## Comparison Requirement

The graph output should be similar to the existing deterministic output.

If differences exist, document them clearly.

| Comparison Area | Expected |
|---|---|
| Final recommendation | Same or explainable difference |
| Risk/score/rank | Same or explainable difference |
| Agent trace | Same sequence or graph-enhanced sequence |
| Shared context | Same accumulated context |
| Audit | Same or additional graph audit reference |
