import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getDashboardSummary, getGovernanceSummary, getPriorityQueue, runCaseReview } from '../api/client'
import { MetricCard } from '../components/MetricCard'
import { StatusBadge } from '../components/StatusBadge'
import type { DashboardSummary, DecisionRecommendation, GovernanceSummary, PriorityQueueResponse } from '../types/ahip'

export function DashboardView() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [governanceSummary, setGovernanceSummary] = useState<GovernanceSummary | null>(null)
  const [recommendations, setRecommendations] = useState<DecisionRecommendation[]>([])
  const [agentResult, setAgentResult] = useState<any>(null)
  const [caseId, setCaseId] = useState('CLM2001')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(error => setError(error.message))
    getGovernanceSummary().then(setGovernanceSummary).catch(console.error)
    getPriorityQueue()
      .then((data: PriorityQueueResponse) => setRecommendations(data.recommendations || []))
      .catch(console.error)
  }, [])

  async function handleRunAgents() {
    setAgentResult(await runCaseReview(caseId))
    const queue = await getPriorityQueue()
    setRecommendations(queue.recommendations || [])
  }

  const highRiskPreview = recommendations.filter(item => ['Critical', 'High'].includes(item.priority)).slice(0, 5)

  return (
    <>
      <span className="badge">Operations Dashboard</span>
      <h2>AHIP Operations Dashboard</h2>
      <p>Executive and operational view of healthcare workflow risk, recommendations, and governance signals.</p>

      {error && <p className="error-state">{error}</p>}

      {summary && (
        <>
          <h3>Executive Summary</h3>
          <div className="grid">
            <MetricCard label="Open Cases" value={summary.open_cases} />
            <MetricCard label="High Risk" value={summary.high_risk_cases} />
            <MetricCard label="Claim Exceptions" value={summary.claim_exceptions} />
            <MetricCard label="Contract Issues" value={summary.provider_contract_issues} />
            <MetricCard label="Compliance Gaps" value={summary.compliance_gaps} />
          </div>
        </>
      )}

      <h3>Operations Metrics</h3>
      <div className="grid">
        <MetricCard label="Queue Items" value={recommendations.length} />
        <MetricCard label="Critical Priority" value={recommendations.filter(item => item.priority === 'Critical').length} />
        <MetricCard label="High Priority" value={recommendations.filter(item => item.priority === 'High').length} />
        <MetricCard label="Accepted" value={governanceSummary?.accepted_recommendations || 0} />
        <MetricCard label="Overrides" value={governanceSummary?.overridden_recommendations || 0} />
      </div>

      <section className="section">
        <div className="section-heading">
          <h3>High-Risk Queue Preview</h3>
          <Link to="/risk-queue">View full queue</Link>
        </div>
        {highRiskPreview.length === 0 ? (
          <p className="empty-state">No critical or high-priority recommendations are available yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Case</th>
                <th>Risk</th>
                <th>Priority</th>
                <th>Owner</th>
                <th>Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {highRiskPreview.map(item => (
                <tr key={item.case_id}>
                  <td><Link to={`/case/${item.case_id}`}>{item.case_id}</Link></td>
                  <td><StatusBadge value={item.risk_level} /></td>
                  <td><StatusBadge value={item.priority} /></td>
                  <td>{item.escalation_owner}</td>
                  <td>{item.recommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {governanceSummary && (
        <section className="section">
          <h3>Governance Summary</h3>
        <div className="grid">
            <MetricCard label="Audit Events" value={governanceSummary.total_audit_events} />
            <MetricCard label="Pending Reviews" value={governanceSummary.pending_recommendations} />
            <MetricCard label="Accepted" value={governanceSummary.accepted_recommendations} />
            <MetricCard label="Overrides" value={governanceSummary.overridden_recommendations} />
        </div>
        </section>
      )}

      <section className="section">
        <h3>Workflow Action</h3>
        <p>Run the deterministic multi-agent review for a known case and refresh the priority queue.</p>
        <div className="action-row">
          <input value={caseId} onChange={(event: any) => setCaseId(event.target.value)} />
        <button onClick={handleRunAgents}>Run Sample Case Review</button>
        </div>
        {agentResult && <pre>{JSON.stringify(agentResult, null, 2)}</pre>}
      </section>

      <section className="section">
        <h3>Product Boundary</h3>
        <p>AHIP is not a chatbot, not a generic RAG system, and not a medical diagnosis tool.</p>
      </section>
    </>
  )
}
