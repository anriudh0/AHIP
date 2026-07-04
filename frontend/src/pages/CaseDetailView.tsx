import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getCaseContext, getExecutionHistory, getPriorityQueue } from '../api/client'
import { AgentTimeline } from '../components/AgentTimeline'
import { StatusBadge } from '../components/StatusBadge'
import type {
  AgentExecution,
  CaseContextResponse,
  DecisionRecommendation,
  PriorityQueueResponse,
} from '../types/ahip'

function collectEvidence(executions: AgentExecution[]) {
  return executions.flatMap(execution => {
    const evidence = execution.output.evidence
    if (Array.isArray(evidence)) return evidence.map(String)
    return []
  })
}

function JsonBlock({ value }: { value: unknown }) {
  return <pre>{JSON.stringify(value, null, 2)}</pre>
}

export function CaseDetailView() {
  const { caseId = '' } = useParams()
  const [context, setContext] = useState<CaseContextResponse | null>(null)
  const [recommendation, setRecommendation] = useState<DecisionRecommendation | null>(null)
  const [executions, setExecutions] = useState<AgentExecution[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!caseId) return

    Promise.all([
      getCaseContext(caseId),
      getPriorityQueue(),
      getExecutionHistory(),
    ])
      .then(([contextData, queueData, historyData]: [CaseContextResponse, PriorityQueueResponse, AgentExecution[]]) => {
        setContext(contextData)
        setRecommendation((queueData.recommendations || []).find(item => item.case_id === caseId) || null)
        setExecutions((historyData || []).filter(item => item.case_id === caseId))
      })
      .catch(error => setError(error.message))
  }, [caseId])

  const evidence = useMemo(() => collectEvidence(executions), [executions])

  return (
    <>
      <Link to="/risk-queue">Back to Risk Queue</Link>
      <div className="case-header">
        <div>
          <span className="badge">Case Detail</span>
          <h2>{caseId}</h2>
        </div>
        {recommendation && (
          <div className="case-badges">
            <StatusBadge value={recommendation.risk_level} />
            <StatusBadge value={recommendation.priority} />
          </div>
        )}
      </div>

      {error && <p className="error-state">{error}</p>}

      <section className="section">
        <h3>Consolidated Recommendation</h3>
        {recommendation ? (
          <div className="detail-grid">
            <div>
              <p className="field-label">Recommendation</p>
              <p>{recommendation.recommendation}</p>
            </div>
            <div>
              <p className="field-label">Escalation Owner</p>
              <p>{recommendation.escalation_owner}</p>
            </div>
            <div>
              <p className="field-label">Risk Score</p>
              <p>{recommendation.risk_score}</p>
            </div>
            <div>
              <p className="field-label">Source Agents</p>
              <p>{recommendation.source_agents.join(', ') || 'Not available'}</p>
            </div>
          </div>
        ) : (
          <p className="empty-state">No consolidated recommendation is available for this case yet.</p>
        )}
      </section>

      <section className="section">
        <h3>Evidence And Explainability</h3>
        <div className="split-grid">
          <div>
            <h4>Evidence</h4>
            {evidence.length ? (
              <ul>{evidence.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul>
            ) : (
              <p className="empty-state">No execution evidence is available yet.</p>
            )}
          </div>
          <div>
            <h4>Explainability Notes</h4>
            {recommendation?.explainability_notes.length ? (
              <ul>{recommendation.explainability_notes.map(note => <li key={note}>{note}</li>)}</ul>
            ) : (
              <p className="empty-state">No explainability notes are available yet.</p>
            )}
          </div>
        </div>
      </section>

      <section className="section">
        <h3>Context Packs</h3>
        {context ? (
          <div className="split-grid">
            <div>
              <h4>Claim Context</h4>
              <JsonBlock value={context.claim_context} />
            </div>
            <div>
              <h4>Patient Journey Context</h4>
              <JsonBlock value={context.patient_journey_context} />
            </div>
            <div>
              <h4>Compliance Context</h4>
              <JsonBlock value={context.compliance_context} />
            </div>
          </div>
        ) : (
          <p className="empty-state">Context has not loaded for this case.</p>
        )}
      </section>

      <section className="section">
        <h3>Relationship Mapping</h3>
        {context ? (
          <div className="split-grid">
            <div>
              <h4>Nodes</h4>
              <JsonBlock value={context.relationship_map.nodes} />
            </div>
            <div>
              <h4>Edges</h4>
              <JsonBlock value={context.relationship_map.edges} />
            </div>
          </div>
        ) : (
          <p className="empty-state">Relationship mapping has not loaded for this case.</p>
        )}
      </section>

      <section className="section">
        <h3>Agent Timeline</h3>
        <AgentTimeline executions={executions} />
      </section>
    </>
  )
}
