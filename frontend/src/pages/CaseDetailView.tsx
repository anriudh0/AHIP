import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, BookOpenCheck, Database, Layers3, ListChecks, Route as RouteIcon, ShieldCheck } from 'lucide-react'
import { getCaseContext, getAuditLogs, getExecutionHistory, getPriorityQueue, runCaseReview } from '../api/client'
import { AgentTimeline } from '../components/AgentTimeline'
import { StatusBadge } from '../components/StatusBadge'
import type {
  AgentExecution,
  AuditLog,
  CaseContextResponse,
  ConsolidatedCaseOutput,
  DecisionRecommendation,
  PriorityQueueResponse,
  SharedMemoryState,
  WorkflowRunResponse,
} from '../types/ahip'

function collectEvidence(executions: AgentExecution[]) {
  return executions.flatMap(execution => {
    const evidence = execution.output.evidence
    if (Array.isArray(evidence)) return evidence.map(String)
    return []
  })
}

function JsonBlock({ value }: { value: unknown }) {
  return <pre className="json-panel">{JSON.stringify(value, null, 2)}</pre>
}

function getLatestWorkflowExecutions(executions: AgentExecution[]) {
  const agentOrder = [
    'Patient Journey Agent',
    'Claims Review Agent',
    'Provider Contract Agent',
    'Consolidator Agent',
  ]

  const orderedExecutions = [...executions].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  )

  const latestByAgent = new Map<string, AgentExecution>()
  for (const execution of orderedExecutions) {
    if (!agentOrder.includes(execution.agent_name)) continue
    if (!latestByAgent.has(execution.agent_name)) {
      latestByAgent.set(execution.agent_name, execution)
      if (latestByAgent.size === agentOrder.length) break
    }
  }

  return agentOrder
    .filter(agentName => latestByAgent.has(agentName))
    .map(agentName => latestByAgent.get(agentName)!)
}

function SummaryValue({ label, value }: { label: string; value: string | number | undefined | null }) {
  return (
    <div className="detail-card">
      <p className="field-label">{label}</p>
      <strong>{value ?? 'N/A'}</strong>
    </div>
  )
}

export function CaseDetailView() {
  const { caseId = '' } = useParams()
  const [context, setContext] = useState<CaseContextResponse | null>(null)
  const [recommendation, setRecommendation] = useState<DecisionRecommendation | null>(null)
  const [executions, setExecutions] = useState<AgentExecution[]>([])
  const [sharedMemory, setSharedMemory] = useState<SharedMemoryState | null>(null)
  const [consolidatedOutput, setConsolidatedOutput] = useState<ConsolidatedCaseOutput | null>(null)
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([])
  const [workflowRun, setWorkflowRun] = useState<WorkflowRunResponse | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!caseId) return

    Promise.all([
      getCaseContext(caseId),
      getPriorityQueue(),
      getExecutionHistory(),
      getAuditLogs(),
    ])
      .then(([contextData, queueData, historyData, auditData]: [CaseContextResponse, PriorityQueueResponse, AgentExecution[], AuditLog[]]) => {
        setContext(contextData)
        setRecommendation((queueData.recommendations || []).find(item => item.case_id === caseId) || null)
        setExecutions((historyData || []).filter(item => item.case_id === caseId))
        setAuditLogs((auditData || []).filter(item => item.case_id === caseId))
      })
      .catch(error => setError(error.message))
  }, [caseId])

  const latestExecutions = useMemo(() => getLatestWorkflowExecutions(executions), [executions])
  const evidence = useMemo(() => collectEvidence(latestExecutions), [latestExecutions])
  const uniqueEvidence = useMemo(() => {
    const seen = new Set<string>()
    return evidence.filter(item => {
      if (seen.has(item)) return false
      seen.add(item)
      return true
    })
  }, [evidence])

  async function handleRunWorkflow() {
    if (!caseId) return
    setIsRunning(true)
    setError(null)

    try {
      const runResult = await runCaseReview(caseId)
      setWorkflowRun(runResult)
      setSharedMemory(runResult.shared_memory)
      setConsolidatedOutput(runResult.consolidated_output)
    } catch (err: any) {
      setError(err.message || 'Workflow run failed')
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="page-stack">
      <Link className="back-link" to="/risk-queue"><ArrowLeft size={16} /> Back to Risk Queue</Link>
      <header className="page-header case-detail-header">
        <div>
          <span className="eyebrow">Agent Workflow Console</span>
          <h1>{caseId}</h1>
          <p>Review workflow execution, shared context, agent outputs, recommendation, and audit evidence.</p>
        </div>
        <div className="case-badges">
          <StatusBadge value={workflowRun?.consolidated_output?.risk_level || recommendation?.risk_level || 'Pending'} />
          <StatusBadge value={workflowRun?.consolidated_output ? 'Workflow complete' : 'Ready to run'} />
        </div>
      </header>

      {error && <div className="error-state">{error}</div>}

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Scenario / Input</span>
            <h2>Selected case and run details</h2>
          </div>
          <button className="button button-primary" onClick={handleRunWorkflow} disabled={isRunning || !caseId}>
            {isRunning ? 'Running workflow…' : 'Run workflow'}
          </button>
        </div>
        <div className="detail-grid">
          <SummaryValue label="Selected Case" value={caseId} />
          <SummaryValue label="Workflow Status" value={workflowRun ? 'Completed' : 'Not run'} />
          <SummaryValue label="Workflow Summary" value={workflowRun?.summary || 'Use the run button to execute the workflow'} />
          <SummaryValue label="Recommendation Source" value={recommendation ? 'Persisted queue' : 'Awaiting run'} />
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Shared Workflow Context</span>
            <h2>Workflow memory and agent contributions</h2>
          </div>
          <Database size={22} aria-hidden="true" />
        </div>
        {sharedMemory ? (
          <div className="detail-grid">
            <SummaryValue label="Agent Sequence" value={sharedMemory.agent_sequence.join(' → ')} />
            <SummaryValue label="Recorded Risks" value={sharedMemory.risk_levels.join(', ')} />
            <SummaryValue label="Recommendations" value={sharedMemory.recommendations.join(' | ')} />
            <SummaryValue label="Current Next Owners" value={sharedMemory.next_owners.join(', ')} />
          </div>
        ) : (
          <div className="empty-state"><Database size={24} /><strong>No shared workflow context</strong><p>Run the workflow to populate shared memory from agent executions.</p></div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Agent Outputs</span>
            <h2>Individual agent results</h2>
          </div>
        </div>
        {workflowRun?.agent_outputs.length ? (
          <div className="split-grid">
            {workflowRun.agent_outputs.map(output => (
              <div key={output.agent_name} className="detail-card">
                <p className="field-label">Agent Name</p>
                <strong>{output.agent_name}</strong>
                <p className="field-label">Status</p>
                <StatusBadge value={output.risk_level} />
                <p className="field-label">Input Used</p>
                <strong>{output.agent_name === 'Patient Journey Agent' ? 'Journey context' : output.agent_name === 'Claims Review Agent' ? 'Claim context' : output.agent_name === 'Provider Contract Agent' ? 'Contract context' : 'Consolidated shared memory'}</strong>
                <p className="field-label">Output Summary</p>
                <strong>{output.observation}</strong>
                <p className="field-label">Reason</p>
                <strong>{output.recommendation}</strong>
                <p className="field-label">Context Updated</p>
                <strong>{output.next_owner || 'None'}</strong>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state"><ListChecks size={24} /><strong>No agent outputs</strong><p>Run the workflow to display agent outputs in the console.</p></div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Evidence</span>
            <h2>Unique evidence from latest run</h2>
          </div>
        </div>
        {uniqueEvidence.length ? (
          <ul className="evidence-list">
            {uniqueEvidence.map((item, index) => (
              <li key={`${item}-${index}`}>{item}</li>
            ))}
          </ul>
        ) : (
          <div className="empty-state"><ListChecks size={24} /><strong>No evidence available</strong><p>Evidence entries appear from the latest workflow execution.</p></div>
        )}
      </section>

      <section className="content-section recommendation-panel">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Final Recommendation</span>
            <h2>Decision support output</h2>
          </div>
          <ShieldCheck size={22} aria-hidden="true" />
        </div>
        {consolidatedOutput ? (
          <div className="detail-grid">
            <div className="detail-card span-2">
              <p className="field-label">Recommendation</p>
              <strong>{consolidatedOutput.recommendation}</strong>
            </div>
            <SummaryValue label="Final Risk Level" value={consolidatedOutput.risk_level} />
            <SummaryValue label="Next Owner" value={consolidatedOutput.next_owner || 'None'} />
            <SummaryValue label="Confidence" value={`${consolidatedOutput.confidence}`} />
            <SummaryValue label="Contributing Agents" value={consolidatedOutput.contributing_agents.join(', ')} />
          </div>
        ) : (
          <div className="empty-state">
            <ListChecks size={24} aria-hidden="true" />
            <strong>No final recommendation</strong>
            <p>Execute the workflow to generate consolidated recommendation output.</p>
          </div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Explanation</span>
            <h2>Why this recommendation was generated</h2>
          </div>
          <BookOpenCheck size={22} aria-hidden="true" />
        </div>
        {recommendation?.explainability_notes.length ? (
          <ul className="evidence-list">{recommendation.explainability_notes.map((note, index) => <li key={`${note}-${index}`}>{note}</li>)}</ul>
        ) : (
          <div className="empty-state"><strong>No explanation available</strong><p>Explanation appears from the recommendation scoring model.</p></div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Audit</span>
            <h2>Governance and trace evidence</h2>
          </div>
        </div>
        {auditLogs.length ? (
          <div className="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Audit ID</th>
                  <th>Event Type</th>
                  <th>Actor Role</th>
                  <th>Actor Name</th>
                  <th>Details</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                {auditLogs.map(log => (
                  <tr key={log.id}>
                    <td>{log.id}</td>
                    <td>{log.event_type}</td>
                    <td>{log.actor_role}</td>
                    <td>{log.actor_name || 'N/A'}</td>
                    <td>{JSON.stringify(log.details)}</td>
                    <td>{new Date(log.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state"><strong>No audit events</strong><p>Audit entries are loaded from the governance audit endpoint.</p></div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Known Limitations</span>
            <h2>Demo boundaries</h2>
          </div>
        </div>
        <div className="detail-grid">
          <SummaryValue label="Workflow Type" value="Deterministic only" />
          <SummaryValue label="LLM Usage" value="None" />
          <SummaryValue label="Recommendation Role" value="Support only" />
          <SummaryValue label="Governance" value="Human review required" />
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Context Packs</span>
            <h2>Purpose-built healthcare context</h2>
          </div>
          <Database size={22} aria-hidden="true" />
        </div>
        {context ? (
          <div className="context-grid">
            <div className="panel-subsection">
              <h3>Claim Context</h3>
              <JsonBlock value={context.claim_context} />
            </div>
            <div className="panel-subsection">
              <h3>Patient Journey Context</h3>
              <JsonBlock value={context.patient_journey_context} />
            </div>
            <div className="panel-subsection">
              <h3>Compliance Context</h3>
              <JsonBlock value={context.compliance_context} />
            </div>
          </div>
        ) : (
          <div className="empty-state"><Database size={24} /><strong>Context not loaded</strong><p>Case context is requested from the existing context endpoint.</p></div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Relationship Mapping</span>
            <h2>Case graph representation</h2>
          </div>
          <Layers3 size={22} aria-hidden="true" />
        </div>
        {context ? (
          <div className="split-grid">
            <div className="panel-subsection">
              <h3>Nodes</h3>
              <JsonBlock value={context.relationship_map.nodes} />
            </div>
            <div className="panel-subsection">
              <h3>Edges</h3>
              <JsonBlock value={context.relationship_map.edges} />
            </div>
          </div>
        ) : (
          <div className="empty-state"><RouteIcon size={24} /><strong>Relationship map not loaded</strong><p>Relationship mapping is available when context loads.</p></div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Agent Timeline</span>
            <h2>Auditable execution history</h2>
          </div>
        </div>
        <AgentTimeline executions={latestExecutions} />
      </section>

      <section className="boundary-panel">
        <ShieldCheck size={20} aria-hidden="true" />
        <div>
          <strong>Workflow controls remain human-reviewed</strong>
          <p>AHIP presents deterministic operational recommendations. Final action remains with the responsible analyst or governance owner.</p>
        </div>
      </section>
    </div>
  )
}
