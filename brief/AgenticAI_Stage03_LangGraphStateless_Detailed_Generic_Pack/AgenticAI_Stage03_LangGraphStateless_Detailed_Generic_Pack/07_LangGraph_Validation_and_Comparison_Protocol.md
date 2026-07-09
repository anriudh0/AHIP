# LangGraph Validation and Comparison Protocol

## Purpose

Validation proves the graph workflow is a safe evolution of the existing deterministic workflow.

## Local Validation Checklist

| No. | Check | Expected Result | Status |
|---:|---|---|---|
| 1 | Backend starts | No errors | Pending |
| 2 | Existing deterministic endpoint works | No regression | Pending |
| 3 | New graph endpoint works | Valid graph response | Pending |
| 4 | Graph state includes input/context | Present | Pending |
| 5 | Graph state includes agent outputs | Present | Pending |
| 6 | Graph output includes final recommendation | Present | Pending |
| 7 | Graph output includes explanation/audit if applicable | Present | Pending |
| 8 | Frontend still works | No regression | Pending |
| 9 | Agent Workflow Console still works | No regression | Pending |
| 10 | Latest Repomix generated | Completed | Pending |

## Old vs Graph Comparison

| Area | Existing Deterministic Output | LangGraph Output | Match? | Notes |
|---|---|---|---|---|
| Final recommendation/result |  |  | Yes / No |  |
| Risk/score/rank |  |  | Yes / No |  |
| Agent sequence |  |  | Yes / No |  |
| Shared context |  |  | Yes / No |  |
| Explanation |  |  | Yes / No |  |
| Audit/reference |  |  | Yes / No |  |

## 4–5 Line Validation Summary

```text
1. Existing deterministic workflow was validated to confirm no regression.
2. New LangGraph stateless endpoint was executed with the same input.
3. Graph state showed domain input, agent node outputs, shared context and final result.
4. Graph output was compared with existing deterministic workflow output.
5. Latest Repomix and validation evidence were captured.
```

## Failure Conditions

Do not close the stage if:

- Existing workflow is broken
- Graph endpoint fails
- Graph output does not include agent trace/state
- Graph result differs without explanation
- LLM was added accidentally
- Latest Repomix is missing
