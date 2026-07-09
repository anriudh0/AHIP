<h1>Post 3 — LangGraph Stateless Implementation</h1>
<p class="lead">Implement the stateless graph by wrapping existing deterministic agents as LangGraph nodes.</p>

<h2>Implementation Objective</h2>
<p>The goal is to add a graph orchestration layer while preserving the existing deterministic workflow.</p>

<h2>Recommended Implementation Structure</h2>
<pre>backend/app/application/graphs/
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
    audit_node.py</pre>

<h2>Implementation Steps</h2>
<table>
<thead><tr><th>Step</th><th>Action</th><th>Status</th></tr></thead>
<tbody>
<tr><td>1</td><td>Add LangGraph dependency if not present.</td><td>Pending</td></tr>
<tr><td>2</td><td>Create graph state schema.</td><td>Pending</td></tr>
<tr><td>3</td><td>Create node wrappers around existing agents.</td><td>Pending</td></tr>
<tr><td>4</td><td>Create graph builder with nodes and edges.</td><td>Pending</td></tr>
<tr><td>5</td><td>Create graph runner service.</td><td>Pending</td></tr>
<tr><td>6</td><td>Add graph API endpoint.</td><td>Pending</td></tr>
<tr><td>7</td><td>Preserve existing endpoint.</td><td>Pending</td></tr>
<tr><td>8</td><td>Run old workflow and graph workflow with same input.</td><td>Pending</td></tr>
<tr><td>9</td><td>Compare outputs.</td><td>Pending</td></tr>
<tr><td>10</td><td>Generate latest Repomix.</td><td>Pending</td></tr>
</tbody>
</table>

<h2>Graph Endpoint Response</h2>
<table>
<thead><tr><th>Field</th><th>Required?</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>workflow_id</code> / <code>case_id</code></td><td>Yes</td><td>Run identifier.</td></tr>
<tr><td><code>graph_mode</code></td><td>Yes</td><td>Shows LangGraph/stateless mode.</td></tr>
<tr><td><code>shared_state</code></td><td>Yes</td><td>Shows graph state.</td></tr>
<tr><td><code>agent_trace</code></td><td>Yes</td><td>Shows node/agent sequence.</td></tr>
<tr><td><code>final_output</code></td><td>Yes</td><td>Final recommendation/result.</td></tr>
<tr><td><code>explanation</code></td><td>Preferred</td><td>Readable reason.</td></tr>
<tr><td><code>audit_reference</code></td><td>Preferred</td><td>Traceability.</td></tr>
</tbody>
</table>

<h2>Master Implementation Prompt</h2>
<pre>Act as a LangGraph Architect, Backend Engineer and RealRails Agentic AI Mentor.

We are implementing Stage 3 — LangGraph Stateless.

Inputs:
1. Latest Repomix
2. Product Foundation feeder
3. Agentic AI Architecture feeder
4. Shared Context / Workflow Memory guide
5. Stage 1.5 visualization evidence
6. Stage 2 cloud evidence
7. Existing workflow API output
8. Known limitations

Task:
Implement a stateless LangGraph workflow using existing deterministic agents.

Rules:
- Do not add LLM.
- Do not rewrite business logic.
- Do not remove existing endpoint.
- Create thin node wrappers around existing agents.
- Define graph state clearly.
- Add a new graph endpoint.
- Return shared state, agent trace and final output.
- Compare graph output with existing deterministic output.

Output:
1. Files to add/change
2. Exact code changes
3. New endpoint details
4. Local run steps
5. Old vs graph comparison steps
6. Evidence checklist
7. Completion report draft</pre>

<div class="warn">Do not close this stage if the old deterministic endpoint breaks.</div>
