<h1>Post 2 — Agent-to-Node Mapping and Graph State Design</h1>
<p class="lead">Before coding, map existing agents to graph nodes and design the shared graph state.</p>

<div class="note">The quality of LangGraph implementation depends on state design. The graph should make existing shared context explicit, not create unrelated new logic.</div>

<h2>Agent-to-Node Mapping</h2>
<table>
<thead><tr><th>Existing Agent/Service</th><th>Current File</th><th>Current Method</th><th>Graph Node Name</th><th>Reads From State</th><th>Writes To State</th></tr></thead>
<tbody>
<tr><td>Agent 1</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Agent 2</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Agent 3</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Recommendation / Consolidator</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Explanation / Audit</td><td></td><td></td><td></td><td></td><td></td></tr>
</tbody>
</table>

<h2>Graph State Requirements</h2>
<table>
<thead><tr><th>State Field</th><th>Purpose</th><th>Required?</th></tr></thead>
<tbody>
<tr><td><code>workflow_id</code> / <code>case_id</code></td><td>Tracks one workflow run.</td><td>Yes</td></tr>
<tr><td><code>domain_input</code></td><td>Original request/case/candidate/passenger input.</td><td>Yes</td></tr>
<tr><td><code>shared_context</code></td><td>Accumulated context/memory.</td><td>Yes</td></tr>
<tr><td><code>agent_outputs</code></td><td>Trace/output from each node.</td><td>Yes</td></tr>
<tr><td><code>final_recommendation</code></td><td>Final decision-support output.</td><td>Yes</td></tr>
<tr><td><code>explanation</code></td><td>Human-readable reason.</td><td>Preferred</td></tr>
<tr><td><code>audit_reference</code></td><td>Traceability link/reference.</td><td>Preferred</td></tr>
<tr><td><code>errors</code></td><td>Controlled error capture.</td><td>Preferred</td></tr>
</tbody>
</table>

<h2>Generic Graph Flow</h2>
<pre>START
→ Context Builder Node
→ Agent 1 Node
→ Agent 2 Node
→ Agent 3 Node
→ Consolidator / Recommendation Node
→ Explanation / Audit Node
→ END</pre>

<h2>Node Wrapper Rule</h2>
<pre>A node should:
1. Read the current graph state.
2. Call the existing deterministic agent/service.
3. Write the result back to graph state.
4. Return the updated state.</pre>

<h2>Design Prompt</h2>
<pre>Act as a LangGraph Architect and Agentic AI Workflow Designer.

Using the latest Repomix and feeder documents, create the LangGraph design before implementation.

Return:
1. Existing workflow summary
2. Agent-to-node mapping table
3. Graph state schema
4. Graph edge sequence
5. New graph endpoint proposal
6. Old vs graph comparison plan

Rules:
- Do not add LLM.
- Do not rewrite existing agent logic.
- Keep graph stateless.
- Preserve existing endpoint.
- Use project-specific domain names.</pre>

<div class="good">After this mapping is approved, proceed to implementation.</div>
