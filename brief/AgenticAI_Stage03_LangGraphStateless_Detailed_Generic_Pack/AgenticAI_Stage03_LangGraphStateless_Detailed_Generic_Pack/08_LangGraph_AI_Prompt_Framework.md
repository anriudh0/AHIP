# LangGraph AI Prompt Framework

## Master Prompt

```text
Act as a LangGraph Architect, Agentic AI Workflow Engineer, Backend Refactoring Mentor and RealRails Internship Mentor.

We are at Stage 3 — LangGraph Stateless.

The project already has:
1. A deterministic Agentic AI MVP
2. A proper Agent Workflow Console from Stage 1.5
3. A cloud-demo-ready deployment from Stage 2
4. Existing agents/orchestrators/services in the backend

Inputs I am providing:
1. Latest Repomix after cloud deployment
2. Product Foundation feeder
3. Agentic AI Architecture feeder
4. Shared Context / Workflow Memory guide
5. Stage 1.5 visualization evidence
6. Stage 2 cloud deployment evidence
7. Existing workflow API output
8. Existing agent trace output
9. Known limitations

Task:
Convert the existing deterministic agent workflow into a LangGraph-style stateless graph.

Requirements:
1. Do not rewrite existing agent business logic.
2. Wrap existing agents/services as graph nodes.
3. Define a graph state schema.
4. Build graph edges in the same order as the existing workflow.
5. Add a new graph workflow endpoint.
6. Keep the existing deterministic endpoint working.
7. Return graph state, agent trace, final output, explanation and audit reference if available.
8. Compare graph output with existing deterministic output.
9. Update README/completion notes.
10. Generate latest Repomix after changes.

Rules:
- Do not add LLM in this stage.
- Do not add long-term checkpointing unless explicitly required.
- Do not break existing APIs.
- Do not remove existing UI.
- Do not change deterministic scoring/rules unless fixing a bug.
- Keep implementation simple and explainable.
- This is stateless graph orchestration, not production autonomous AI.

Output required:
1. Current workflow assessment
2. Agent-to-node mapping table
3. Graph state design
4. Files to add/change
5. Exact code changes
6. New graph endpoint details
7. Local validation steps
8. Old vs graph comparison steps
9. Evidence checklist
10. Completion report draft
```

## Debugging Prompt

```text
The LangGraph implementation is failing.

I am attaching:
1. Latest Repomix after attempted LangGraph changes
2. Error logs
3. Existing deterministic endpoint response
4. Graph endpoint response/error
5. Files changed
6. Expected behavior
7. Actual behavior

Please debug with minimal changes.

Rules:
- Do not rewrite unrelated code.
- Do not change deterministic agent logic.
- Do not add LLM.
- Preserve existing endpoint.
- Fix graph implementation only.
- Provide exact file-level changes and validation steps.
```
