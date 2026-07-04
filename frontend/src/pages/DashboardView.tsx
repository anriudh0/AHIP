import { useEffect, useState } from 'react'
import { getDashboardSummary, runCaseReview } from '../api/client'
import { MetricCard } from '../components/MetricCard'
import type { DashboardSummary } from '../types/ahip'

export function DashboardView() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [agentResult, setAgentResult] = useState<any>(null)

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(console.error)
  }, [])

  async function handleRunAgents() {
    setAgentResult(await runCaseReview('CASE-001'))
  }

  return (
    <>
      <span className="badge">Phase 1 Base</span>
      <h2>AHIP Operations Dashboard</h2>
      <p>This is the frontend baseline for the healthcare workflow intelligence platform.</p>

      {summary && (
        <div className="grid">
          <MetricCard label="Open Cases" value={summary.open_cases} />
          <MetricCard label="High Risk" value={summary.high_risk_cases} />
          <MetricCard label="Claim Exceptions" value={summary.claim_exceptions} />
          <MetricCard label="Contract Issues" value={summary.provider_contract_issues} />
          <MetricCard label="Compliance Gaps" value={summary.compliance_gaps} />
        </div>
      )}

      <section className="section">
        <h3>Sample Multi-Agent Workflow</h3>
        <p>Run a Phase 0 sample case review.</p>
        <button onClick={handleRunAgents}>Run Sample Case Review</button>
        {agentResult && <pre>{JSON.stringify(agentResult, null, 2)}</pre>}
      </section>

      <section className="section">
        <h3>Boundary</h3>
        <p>AHIP is not a chatbot, not a generic RAG system, and not a medical diagnosis tool.</p>
      </section>
    </>
  )
}
