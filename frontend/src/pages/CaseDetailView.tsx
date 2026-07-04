import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, BookOpenCheck, Database, Layers3, ListChecks, Route as RouteIcon, ShieldCheck } from 'lucide-react'
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
  return <pre className="json-panel">{JSON.stringify(value, null, 2)}</pre>
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
    <div className="page-stack">
      <Link className="back-link" to="/risk-queue"><ArrowLeft size={16} /> Back to Risk Queue</Link>
      <header className="page-header case-detail-header">
        <div>
          <span className="eyebrow">Case Detail</span>
          <h1>{caseId}</h1>
          <p>Analyst workspace for consolidated recommendation, evidence, context, relationships, and agent execution history.</p>
        </div>
        {recommendation && (
          <div className="case-badges">
            <StatusBadge value={recommendation.risk_level} />
            <StatusBadge value={recommendation.priority} />
          </div>
        )}
      </header>

      {error && <div className="error-state">{error}</div>}

      <section className="content-section recommendation-panel">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Recommendation Summary</span>
            <h2>Consolidated case recommendation</h2>
          </div>
          <ShieldCheck size={22} aria-hidden="true" />
        </div>
        {recommendation ? (
          <div className="detail-grid">
            <div className="detail-card span-2">
              <p className="field-label">Recommendation</p>
              <strong>{recommendation.recommendation}</strong>
            </div>
            <div className="detail-card">
              <p className="field-label">Escalation Owner</p>
              <strong>{recommendation.escalation_owner}</strong>
            </div>
            <div className="detail-card">
              <p className="field-label">Risk Score</p>
              <strong>{recommendation.risk_score}</strong>
            </div>
            <div className="detail-card">
              <p className="field-label">Source Agents</p>
              <strong>{recommendation.source_agents.join(', ') || 'Not available'}</strong>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <ListChecks size={24} aria-hidden="true" />
            <strong>No consolidated recommendation</strong>
            <p>Run the case review workflow from the dashboard to generate a recommendation.</p>
          </div>
        )}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Evidence</span>
            <h2>Explainability and supporting signals</h2>
          </div>
          <BookOpenCheck size={22} aria-hidden="true" />
        </div>
        <div className="split-grid">
          <div className="panel-subsection">
            <h3>Evidence</h3>
            {evidence.length ? (
              <ul className="evidence-list">{evidence.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul>
            ) : (
              <div className="empty-state compact"><strong>No evidence yet</strong><p>Evidence appears after agent execution.</p></div>
            )}
          </div>
          <div className="panel-subsection">
            <h3>Explainability Notes</h3>
            {recommendation?.explainability_notes.length ? (
              <ul className="evidence-list">{recommendation.explainability_notes.map(note => <li key={note}>{note}</li>)}</ul>
            ) : (
              <div className="empty-state compact"><strong>No explainability notes yet</strong><p>Scoring notes appear with the recommendation.</p></div>
            )}
          </div>
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
        <AgentTimeline executions={executions} />
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
