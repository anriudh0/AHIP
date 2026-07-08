import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertTriangle, BarChart3, ClipboardList, FileText, Gauge, ShieldCheck } from 'lucide-react'
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

  const dedupedRecommendations = (() => {
    // reuse RiskQueueView deduplication: keep latest recommendation per case_id
    const latestByCase = new Map<string, DecisionRecommendation>()
    for (let i = recommendations.length - 1; i >= 0; i -= 1) {
      const item = recommendations[i]
      if (!latestByCase.has(item.case_id)) latestByCase.set(item.case_id, item)
    }
    const deduped: DecisionRecommendation[] = []
    for (const item of recommendations) {
      if (latestByCase.get(item.case_id) === item) deduped.push(item)
    }
    return deduped
  })()

  async function handleRunAgents() {
    setAgentResult(await runCaseReview(caseId))
    const queue = await getPriorityQueue()
    setRecommendations(queue.recommendations || [])
  }

  const highRiskPreview = dedupedRecommendations.filter(item => ['Critical', 'High'].includes(item.priority)).slice(0, 5)

  return (
    <div className="page-stack">
      <header className="page-hero">
        <div>
          <span className="eyebrow">Operations Dashboard</span>
          <h1>Healthcare operations intelligence</h1>
          <p>Monitor agent-driven recommendations, workflow risk, governance signals, and case review activity from one executive workspace.</p>
        </div>
        <div className="hero-stat">
          <span>Queue Health</span>
          <strong>{recommendations.length}</strong>
          <p>active recommendations</p>
        </div>
      </header>

      {error && <div className="error-state">{error}</div>}

      {summary && (
        <section className="content-section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">Executive Summary</span>
              <h2>Operational signal overview</h2>
            </div>
          </div>
          <div className="metric-grid">
            <MetricCard icon={ClipboardList} label="Open Cases" value={summary.open_cases} detail="care and workflow tasks" />
            <MetricCard icon={AlertTriangle} label="High Risk" value={summary.high_risk_cases} detail="members flagged high risk" />
            <MetricCard icon={FileText} label="Claim Exceptions" value={summary.claim_exceptions} detail="pended claim activity" />
            <MetricCard icon={ShieldCheck} label="Contract Issues" value={summary.provider_contract_issues} detail="provider contract signals" />
            <MetricCard icon={Gauge} label="Compliance Gaps" value={summary.compliance_gaps} detail="documentation review" />
          </div>
        </section>
      )}

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Operations Metrics</span>
            <h2>Recommendation workload</h2>
          </div>
        </div>
        <div className="metric-grid">
          <MetricCard icon={BarChart3} label="Queue Items" value={recommendations.length} detail="total recommendations" />
          <MetricCard icon={AlertTriangle} label="Critical Priority" value={recommendations.filter(item => item.priority === 'Critical').length} detail="requires immediate review" />
          <MetricCard icon={ShieldCheck} label="High Priority" value={recommendations.filter(item => item.priority === 'High').length} detail="elevated workflow risk" />
          <MetricCard icon={ClipboardList} label="Accepted" value={governanceSummary?.accepted_recommendations || 0} detail="human-reviewed decisions" />
          <MetricCard icon={FileText} label="Overrides" value={governanceSummary?.overridden_recommendations || 0} detail="manual governance actions" />
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">High-Risk Queue Preview</span>
            <h2>Cases needing attention</h2>
          </div>
          <Link className="button button-secondary" to="/risk-queue">View full queue</Link>
        </div>
        {highRiskPreview.length === 0 ? (
          <div className="empty-state">
            <AlertTriangle size={24} aria-hidden="true" />
            <strong>No elevated recommendations yet</strong>
            <p>Run a case review to populate the high-risk queue preview.</p>
          </div>
        ) : (
          <div className="table-shell">
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
          </div>
        )}
      </section>

      {governanceSummary && (
        <section className="content-section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">Governance Summary</span>
              <h2>Decision review posture</h2>
            </div>
          </div>
          <div className="metric-grid compact">
            <MetricCard label="Audit Events" value={governanceSummary.total_audit_events} />
            <MetricCard label="Pending Reviews" value={governanceSummary.pending_recommendations} />
            <MetricCard label="Accepted" value={governanceSummary.accepted_recommendations} />
            <MetricCard label="Overrides" value={governanceSummary.overridden_recommendations} />
          </div>
        </section>
      )}

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Workflow Actions</span>
            <h2>Run deterministic case review</h2>
            <p>Trigger the existing multi-agent pipeline and refresh the recommendation queue.</p>
          </div>
        </div>
        <div className="form-panel">
          <label>
            Case ID
            <input value={caseId} onChange={(event: any) => setCaseId(event.target.value)} placeholder="CLM2001" />
          </label>
          <button className="button button-primary" onClick={handleRunAgents}>Run Case Review</button>
        </div>
        {agentResult && <pre className="json-panel">{JSON.stringify(agentResult, null, 2)}</pre>}
      </section>

      <section className="boundary-panel">
        <ShieldCheck size={20} aria-hidden="true" />
        <div>
          <strong>Governance-first product boundary</strong>
          <p>AHIP is not a chatbot, not a generic RAG system, and not a medical diagnosis tool. Recommendations remain operational and human-reviewed.</p>
        </div>
      </section>
    </div>
  )
}
