import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertTriangle, Filter, Search, ShieldAlert } from 'lucide-react'
import { getPriorityQueue } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'
import type { DecisionRecommendation, PriorityQueueResponse } from '../types/ahip'

function operationalStatus(item: DecisionRecommendation) {
  return ['Critical', 'High'].includes(item.priority) ? 'Escalated' : 'Open Review'
}

export function RiskQueueView() {
  const [recommendations, setRecommendations] = useState<DecisionRecommendation[]>([])
  const [riskFilter, setRiskFilter] = useState('All')
  const [priorityFilter, setPriorityFilter] = useState('All')
  const [statusFilter, setStatusFilter] = useState('All')
  const [caseSearch, setCaseSearch] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getPriorityQueue()
      .then((data: PriorityQueueResponse) => setRecommendations(data.recommendations || []))
      .catch(error => setError(error.message))
  }, [])

  const filteredRecommendations = useMemo(() => {
    return recommendations.filter(item => {
      const matchesRisk = riskFilter === 'All' || item.risk_level === riskFilter
      const matchesPriority = priorityFilter === 'All' || item.priority === priorityFilter
      const matchesStatus = statusFilter === 'All' || operationalStatus(item) === statusFilter
      const matchesCase = item.case_id.toLowerCase().includes(caseSearch.trim().toLowerCase())
      return matchesRisk && matchesPriority && matchesStatus && matchesCase
    })
  }, [caseSearch, priorityFilter, recommendations, riskFilter, statusFilter])

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Risk Queue</span>
          <h1>Prioritized case recommendations</h1>
          <p>Review deterministic recommendations by risk level, priority, owner, and operational status.</p>
        </div>
        <div className="header-chip">
          <ShieldAlert size={18} />
          {filteredRecommendations.length} visible
        </div>
      </header>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Filters</span>
            <h2>Focus the work queue</h2>
          </div>
          <Filter size={20} aria-hidden="true" />
        </div>
        <div className="filters">
          <label className="search-field">
            Case ID
            <span>
              <Search size={16} aria-hidden="true" />
              <input value={caseSearch} onChange={(event: any) => setCaseSearch(event.target.value)} placeholder="Search case" />
            </span>
          </label>
          <label>
            Risk
            <select value={riskFilter} onChange={(event: any) => setRiskFilter(event.target.value)}>
              <option>All</option>
              <option>Critical</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </label>
          <label>
            Priority
            <select value={priorityFilter} onChange={(event: any) => setPriorityFilter(event.target.value)}>
              <option>All</option>
              <option>Critical</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </label>
          <label>
            Status
            <select value={statusFilter} onChange={(event: any) => setStatusFilter(event.target.value)}>
              <option>All</option>
              <option>Escalated</option>
              <option>Open Review</option>
            </select>
          </label>
        </div>
      </section>

      {error && <div className="error-state">{error}</div>}

      <section className="content-section">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Recommendations</span>
            <h2>Highest priority first</h2>
          </div>
        </div>
        {filteredRecommendations.length === 0 ? (
          <div className="empty-state">
            <AlertTriangle size={24} aria-hidden="true" />
            <strong>No recommendations found</strong>
            <p>Adjust filters or run a case review from the dashboard to populate the queue.</p>
          </div>
        ) : (
          <div className="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Risk</th>
                  <th>Score</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Owner</th>
                  <th>Recommendation</th>
                </tr>
              </thead>
              <tbody>
                {filteredRecommendations.map(item => (
                  <tr key={item.case_id}>
                    <td><Link to={`/case/${item.case_id}`}>{item.case_id}</Link></td>
                    <td><StatusBadge value={item.risk_level} /></td>
                    <td><strong>{item.risk_score}</strong></td>
                    <td><StatusBadge value={item.priority} /></td>
                    <td><StatusBadge value={operationalStatus(item)} /></td>
                    <td>{item.escalation_owner}</td>
                    <td>{item.recommendation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  )
}
